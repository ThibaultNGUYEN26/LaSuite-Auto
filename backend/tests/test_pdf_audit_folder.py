import csv
import io
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from fpdf import FPDF

from agent.artifact_store import MemoryArtifactStore
from agent.artifacts import Artifact
from agent.base import DelegationContext
from agent.errors import PdfError
from agent.specialists.local_files.audit_folder import LocalFilesAuditFolderAgent
from services.pdf_memory import save_pdf_memory
from services.pdf_search import pdf_page_cache


def pdf_bytes(text: str) -> bytes:
    pdf = FPDF()
    pdf.set_font("Helvetica", size=12)
    pdf.add_page()
    pdf.multi_cell(0, 8, text)
    return bytes(pdf.output())


class FakeClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    async def chat_completion_stream(self, **request):
        self.requests.append(deepcopy(request))
        yield {"type": "content", "delta": next(self.responses)}
        yield {"type": "done", "tool_calls": []}


class NeverCalledSummarizer:
    async def summarize(self, relative_path: str):
        raise AssertionError(f"Unexpected preparation for {relative_path}")


class FakeBatchSummarizer:
    def __init__(self):
        self.calls = []

    async def execute(self, arguments, context):
        self.calls.append((deepcopy(arguments), context))
        return {
            "status": "completed",
            "requested": 2,
            "created": 2,
            "updated": 0,
            "skipped": 0,
            "failed": 0,
            "limited": False,
            "limitation": None,
            "results": [],
        }


class PdfFolderAuditTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        pdf_page_cache.clear()

    async def test_audits_every_supported_file_as_one_corpus(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference_path = "AUTO/ISO42001.pdf"
            client_directory = "AUTO/Clients/VAL_Valdorne"
            (root / "AUTO/Clients/VAL_Valdorne").mkdir(parents=True)
            (root / "AUTO/Reports").mkdir()
            (root / reference_path).write_bytes(
                pdf_bytes(
                    "The organization must define its AI scope and assess AI risks."
                )
            )
            (root / client_directory / "D01_scope.pdf").write_bytes(
                pdf_bytes("The AI scope and management responsibility are approved.")
            )
            (root / client_directory / "D02_risks.pdf").write_bytes(
                pdf_bytes("Risk assessment controls and mitigation are reviewed monthly.")
            )
            (root / client_directory / "D10_risk_register.csv").write_text(
                "risk_id,status,owner\nR1,open,Alice\n", encoding="utf-8"
            )
            save_pdf_memory(
                root,
                source_relative_path=reference_path,
                title="ISO 42001 checklist",
                summary_markdown="AI scope and risk assessment requirements [p. 1]",
                total_pages=1,
            )
            client = FakeClient(
                [
                    json.dumps(
                        {
                            "criteria": [
                                {
                                    "name": "AI scope",
                                    "requirement": "Define the AI scope",
                                    "query": "AI scope management responsibility",
                                },
                                {
                                    "name": "Risk assessment",
                                    "requirement": "Assess and mitigate AI risks",
                                    "query": "risk assessment controls mitigation risk owner",
                                },
                            ]
                        }
                    ),
                    json.dumps(
                        {
                            "findings": [
                                {
                                    "criterion_number": 1,
                                    "status": "COMPLIANT",
                                    "requirement": "Define the AI scope",
                                    "reference_evidence": "[AUTO/ISO42001.pdf, p. 1]",
                                    "client_evidence": "[AUTO/Clients/VAL_Valdorne/D01_scope.pdf, p. 1]",
                                    "reasoning": "The scope is defined.",
                                    "corrective_action": "None.",
                                },
                                {
                                    "criterion_number": 2,
                                    "status": "COMPLIANT",
                                    "requirement": "Assess and mitigate AI risks",
                                    "reference_evidence": "[AUTO/ISO42001.pdf, p. 1]",
                                    "client_evidence": "[AUTO/Clients/VAL_Valdorne/D02_risks.pdf, p. 1]; [AUTO/Clients/VAL_Valdorne/D10_risk_register.csv, lines 1-2]",
                                    "reasoning": "Risks and ownership are documented.",
                                    "corrective_action": "None.",
                                },
                            ]
                        }
                    ),
                ]
            )
            batch_summarizer = FakeBatchSummarizer()
            artifact_store = MemoryArtifactStore()
            agent = LocalFilesAuditFolderAgent(
                root,
                NeverCalledSummarizer(),
                api_key=None,
                base_url="http://albert",
                requested_model=None,
                max_read_bytes=1_000_000,
                max_text_characters=100_000,
                max_files=100,
                max_total_pages=100,
                batch_summarizer=batch_summarizer,
                artifact_store=artifact_store,
                client=client,
                model="text-model",
            )

            result = await agent.execute(
                {
                    "audit_relative_path": reference_path,
                    "client_directory": client_directory,
                    "csv_relative_path": "AUTO/Reports/Valdorne_Audit_Matrix.csv",
                },
                DelegationContext(conversation=()),
            )
            csv_text = (
                root / "AUTO/Reports/Valdorne_Audit_Matrix.csv"
            ).read_text(encoding="utf-8")
            audit_payload = artifact_store.get(
                Artifact.model_validate(result["audit_artifact"]),
                expected_kind="audit_report",
            )

        evidence = client.requests[1]["messages"][1]["content"]
        self.assertEqual(result["status"], "audited")
        self.assertEqual(result["criteria_count"], 2)
        self.assertEqual(result["source_count"], 3)
        self.assertEqual(result["pdf_count"], 2)
        self.assertEqual(result["text_count"], 1)
        self.assertTrue(result["complete"])
        self.assertTrue(result["client_memories_complete"])
        self.assertEqual(result["client_memories"]["created"], 2)
        self.assertEqual(
            batch_summarizer.calls[0][0]["directory"], client_directory
        )
        self.assertIn("D01_scope.pdf, p. 1]", evidence)
        self.assertIn("D02_risks.pdf, p. 1]", evidence)
        self.assertIn("D10_risk_register.csv, lines 1-2]", evidence)
        self.assertNotIn("audit", result)
        self.assertNotIn("findings", result)
        self.assertNotIn("criteria", result)
        self.assertEqual(result["audit_artifact"]["kind"], "audit_report")
        self.assertEqual(result["verdict_counts"], {"COMPLIANT": 2})
        self.assertLess(len(json.dumps(result)), 10_000)
        self.assertIn("### 1. AI scope", audit_payload["audit"])
        self.assertIn("### 2. Risk assessment", audit_payload["audit"])
        self.assertIn("## Complete audit matrix", audit_payload["audit"])
        self.assertIn("| Requirement | Verdict | Reference evidence |", audit_payload["audit"])
        self.assertIn("| 2 | Risk assessment |", audit_payload["audit"])
        self.assertIn("## Source register", audit_payload["audit"])
        self.assertIn("| REF | Audit reference | ISO42001.pdf | PDF |", audit_payload["audit"])
        self.assertIn("D10_risk_register.csv", audit_payload["audit"])
        self.assertEqual(len(audit_payload["sources"]), 4)
        self.assertEqual(result["source_register_count"], 4)
        self.assertEqual(audit_payload["sources"][0]["source_id"], "REF")
        self.assertEqual(
            audit_payload["sources"][0]["artifact"]["reference"], reference_path
        )
        evidence_sources = audit_payload["sources"][1:]
        self.assertEqual(
            {source["source_id"] for source in evidence_sources},
            {"SRC-001", "SRC-002", "SRC-003"},
        )
        self.assertEqual(
            {source["artifact"]["reference"] for source in evidence_sources},
            {
                f"{client_directory}/D01_scope.pdf",
                f"{client_directory}/D02_risks.pdf",
                f"{client_directory}/D10_risk_register.csv",
            },
        )
        self.assertTrue(
            all(source["artifact"]["location"] == "local" for source in audit_payload["sources"])
        )
        self.assertEqual(
            result["audit_csv"]["relative_path"],
            "AUTO/Reports/Valdorne_Audit_Matrix.csv",
        )
        self.assertEqual(result["audit_csv"]["artifact"]["media_type"], "text/csv")
        csv_rows = list(csv.reader(io.StringIO(csv_text)))
        self.assertEqual(
            csv_rows[0],
            [
                "criterion",
                "requirement",
                "verdict",
                "reference evidence",
                "client evidence",
                "reasoning",
                "corrective action",
            ],
        )
        self.assertEqual(len(csv_rows), 3)
        self.assertEqual(csv_rows[1][0], "AI scope")

    async def test_rejects_folder_without_supported_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Client").mkdir()
            (root / "Client/image.png").write_bytes(b"png")
            (root / "reference.pdf").write_bytes(pdf_bytes("One requirement"))
            save_pdf_memory(
                root,
                source_relative_path="reference.pdf",
                title="Reference",
                summary_markdown="One requirement [p. 1]",
                total_pages=1,
            )
            agent = LocalFilesAuditFolderAgent(
                root,
                NeverCalledSummarizer(),
                api_key=None,
                base_url="http://albert",
                requested_model=None,
                max_read_bytes=1_000_000,
                max_text_characters=100_000,
                max_files=100,
                max_total_pages=100,
                client=FakeClient([]),
                model="text-model",
            )
            with self.assertRaises(PdfError):
                await agent.execute(
                    {
                        "audit_relative_path": "reference.pdf",
                        "client_directory": "Client",
                    },
                    DelegationContext(conversation=()),
                )


if __name__ == "__main__":
    unittest.main()
