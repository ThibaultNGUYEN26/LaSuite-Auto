import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from fpdf import FPDF

from agent.base import DelegationContext
from agent.specialists.local_files.audit_pdf import LocalFilesAuditPdfAgent
from services.pdf_audit import _parse_criteria
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


class PdfAuditTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        pdf_page_cache.clear()

    def test_does_not_silently_cap_audit_at_twenty_criteria(self):
        raw = json.dumps(
            {
                "criteria": [
                    {
                        "name": f"Criterion {number}",
                        "requirement": f"Requirement {number}",
                        "query": f"evidence term {number}",
                    }
                    for number in range(1, 26)
                ]
            }
        )
        self.assertEqual(len(_parse_criteria(raw)), 25)

    async def test_audits_each_criterion_from_both_original_documents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference_path = "Auditor/requirements.pdf"
            client_path = "Client_2/report.pdf"
            (root / "Auditor").mkdir()
            (root / "Client_2").mkdir()
            (root / reference_path).write_bytes(
                pdf_bytes("Emergency lighting must be tested every month.")
            )
            (root / client_path).write_bytes(
                pdf_bytes("Emergency lighting is tested monthly with signed logs.")
            )
            save_pdf_memory(
                root,
                source_relative_path=reference_path,
                title="Building audit requirements",
                summary_markdown="## Requirements\nMonthly emergency-light tests [p. 1]",
                total_pages=1,
            )
            save_pdf_memory(
                root,
                source_relative_path=client_path,
                title="Client 2 report",
                summary_markdown="## Evidence\nMonthly lighting logs [p. 1]",
                total_pages=1,
            )
            client = FakeClient(
                [
                    json.dumps(
                        {
                            "criteria": [
                                {
                                    "name": "Emergency lighting",
                                    "requirement": "Test emergency lighting monthly",
                                    "query": "emergency lighting monthly tested logs",
                                }
                            ]
                        }
                    ),
                    (
                        "## Emergency lighting — COMPLIANT\n"
                        "Required monthly [requirements.pdf, p. 1]; signed logs are "
                        "reported [report.pdf, p. 1]."
                    ),
                ]
            )
            agent = LocalFilesAuditPdfAgent(
                root,
                NeverCalledSummarizer(),
                api_key=None,
                base_url="http://albert",
                requested_model=None,
                max_read_bytes=1_000_000,
                max_total_pages=100,
                client=client,
                model="text-model",
            )

            result = await agent.execute(
                {
                    "audit_relative_path": reference_path,
                    "client_relative_path": client_path,
                },
                DelegationContext(conversation=()),
            )

        evidence = client.requests[1]["messages"][1]["content"]
        self.assertEqual(result["status"], "audited")
        self.assertEqual(result["criteria_count"], 1)
        self.assertTrue(result["grounded"])
        self.assertEqual(result["documents_prepared"], 0)
        self.assertEqual(result["source_register_count"], 2)
        self.assertEqual(
            [source["source_id"] for source in result["sources"]],
            ["REF", "SRC-001"],
        )
        self.assertEqual(
            result["sources"][1]["artifact"]["reference"], client_path
        )
        self.assertIn("## Source register", result["audit"])
        self.assertIn("`Client_2/report.pdf`", result["audit"])
        self.assertIn("[requirements.pdf, p. 1]", evidence)
        self.assertIn("[report.pdf, p. 1]", evidence)
        self.assertIn("must be tested every month", evidence)
        self.assertIn("tested monthly with signed logs", evidence)


if __name__ == "__main__":
    unittest.main()
