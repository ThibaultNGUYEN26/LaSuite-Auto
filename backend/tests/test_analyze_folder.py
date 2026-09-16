import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from fpdf import FPDF

from agent.base import DelegationContext
from agent.specialists.local_files.analyze_folder import LocalFilesAnalyzeFolderAgent
from services.pdf_memory import save_pdf_memory


def pdf_bytes(text: str) -> bytes:
    pdf = FPDF()
    pdf.set_font("Helvetica", size=12)
    pdf.add_page()
    pdf.multi_cell(0, 8, text)
    return bytes(pdf.output())


class FakeBatchSummarizer:
    def __init__(self):
        self.calls = []

    async def execute(self, arguments, context):
        self.calls.append((deepcopy(arguments), context))
        return {
            "requested": len(arguments["relative_paths"]),
            "created": 0,
            "updated": 0,
            "skipped": len(arguments["relative_paths"]),
            "failed": 0,
            "limited": False,
            "limitation": None,
            "results": [],
        }


class FakeClient:
    def __init__(self, response):
        self.response = response
        self.requests = []

    async def chat_completion_stream(self, **request):
        self.requests.append(deepcopy(request))
        yield {"type": "content", "delta": self.response}
        yield {"type": "done", "tool_calls": []}


class AnalyzeFolderTests(unittest.IsolatedAsyncioTestCase):
    async def test_analyzes_reference_pdf_client_pdf_and_csv_in_one_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            client_directory = "AUTO/Clients/VAL"
            reference_path = "AUTO/ISO42001.pdf"
            client_pdf = f"{client_directory}/01_scope.pdf"
            client_csv = f"{client_directory}/10_risks.csv"
            (root / client_directory).mkdir(parents=True)
            (root / reference_path).write_bytes(pdf_bytes("ISO checklist"))
            (root / client_pdf).write_bytes(pdf_bytes("Client scope"))
            (root / client_csv).write_text(
                "risk,status\nR1,open\n", encoding="utf-8"
            )
            save_pdf_memory(
                root,
                source_relative_path=reference_path,
                title="ISO checklist",
                summary_markdown="Reference overview [p. 1]",
                total_pages=1,
            )
            save_pdf_memory(
                root,
                source_relative_path=client_pdf,
                title="Client scope",
                summary_markdown="Client scope overview [p. 1]",
                total_pages=1,
            )
            summaries = {
                "documents": [
                    {
                        "path": reference_path,
                        "summary": "The checklist describes an AIMS process [p. 1].",
                        "key_points": ["Four phases"],
                    },
                    {
                        "path": client_pdf,
                        "summary": "The document defines the client scope [p. 1].",
                        "key_points": ["Defined scope"],
                    },
                    {
                        "path": client_csv,
                        "summary": f"The register contains one open risk [{client_csv}, lines 1-2].",
                        "key_points": ["R1 is open"],
                    },
                ]
            }
            batch = FakeBatchSummarizer()
            client = FakeClient(json.dumps(summaries))
            agent = LocalFilesAnalyzeFolderAgent(
                root,
                batch,
                api_key=None,
                base_url="http://albert",
                requested_model=None,
                max_read_bytes=1_000_000,
                max_text_characters=100_000,
                max_files=50,
                client=client,
                model="text-model",
            )

            result = await agent.execute(
                {
                    "directory": client_directory,
                    "additional_pdf_paths": [reference_path],
                },
                DelegationContext(conversation=()),
            )

        self.assertTrue(result["complete"])
        self.assertEqual(result["document_count"], 3)
        self.assertEqual(result["pdf_count"], 2)
        self.assertEqual(result["text_count"], 1)
        self.assertEqual(result["pdf_memories"]["requested"], 2)
        self.assertEqual(
            batch.calls[0][0]["relative_paths"], [reference_path, client_pdf]
        )
        self.assertIn(f"## {reference_path}", result["analysis"])
        self.assertIn(f"## {client_pdf}", result["analysis"])
        self.assertIn(f"## {client_csv}", result["analysis"])
        self.assertIn("not an audit", client.requests[0]["messages"][0]["content"])


if __name__ == "__main__":
    unittest.main()
