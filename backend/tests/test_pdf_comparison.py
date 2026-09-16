import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from fpdf import FPDF

from agent.base import DelegationContext
from agent.specialists.local_files.compare_pdfs import LocalFilesComparePdfsAgent
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
        raise AssertionError(f"Unexpected refresh for {relative_path}")


class RecordingSummarizer:
    def __init__(self, root: Path):
        self.root = root
        self.calls = []

    async def summarize(self, relative_path: str):
        self.calls.append(relative_path)
        return save_pdf_memory(
            self.root,
            source_relative_path=relative_path,
            title=Path(relative_path).stem,
            summary_markdown=f"## Overview\nMemory for {relative_path} [p. 1]",
            total_pages=1,
        )


class PdfComparisonTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        pdf_page_cache.clear()

    async def test_compares_original_evidence_from_both_documents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "policy-a.pdf").write_bytes(
                pdf_bytes("The policy requires encryption and annual security audits.")
            )
            (root / "policy-b.pdf").write_bytes(
                pdf_bytes("The policy recommends encryption and quarterly security audits.")
            )
            for name in ("policy-a.pdf", "policy-b.pdf"):
                save_pdf_memory(
                    root,
                    source_relative_path=name,
                    title=name.removesuffix(".pdf"),
                    summary_markdown="## Overview\nEncryption and audit policy [p. 1]",
                    total_pages=1,
                )
            client = FakeClient(
                [
                    json.dumps(
                        {
                            "dimensions": [
                                {
                                    "name": "Security requirements",
                                    "query": "encryption security audit policy",
                                }
                            ]
                        }
                    ),
                    (
                        "## Executive comparison\nBoth discuss encryption. "
                        "[policy-a.pdf, p. 1] [policy-b.pdf, p. 1]"
                    ),
                ]
            )
            agent = LocalFilesComparePdfsAgent(
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
                    "relative_paths": ["policy-a.pdf", "policy-b.pdf"],
                    "focus": "Compare security obligations",
                },
                DelegationContext(conversation=()),
            )

        evidence = client.requests[1]["messages"][1]["content"]
        self.assertEqual(result["status"], "compared")
        self.assertTrue(result["grounded"])
        self.assertEqual(result["memories_created_or_refreshed"], [])
        self.assertIn("[policy-a.pdf, p. 1]", evidence)
        self.assertIn("[policy-b.pdf, p. 1]", evidence)
        self.assertIn("annual security audits", evidence)
        self.assertIn("quarterly security audits", evidence)

    async def test_creates_missing_memories_before_comparing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("one.pdf", "two.pdf"):
                (root / name).write_bytes(pdf_bytes("Shared topic evidence."))
            summarizer = RecordingSummarizer(root)
            client = FakeClient(
                [
                    '{"dimensions":[{"name":"Topic","query":"shared topic evidence"}]}',
                    "## Executive comparison\nShared topic [one.pdf, p. 1] [two.pdf, p. 1]",
                ]
            )
            agent = LocalFilesComparePdfsAgent(
                root,
                summarizer,
                api_key=None,
                base_url="http://albert",
                requested_model=None,
                max_read_bytes=1_000_000,
                max_total_pages=100,
                client=client,
                model="text-model",
            )

            result = await agent.execute(
                {"relative_paths": ["one.pdf", "two.pdf"]},
                DelegationContext(conversation=()),
            )

        self.assertCountEqual(summarizer.calls, ["one.pdf", "two.pdf"])
        self.assertCountEqual(
            result["memories_created_or_refreshed"], ["one.pdf", "two.pdf"]
        )


if __name__ == "__main__":
    unittest.main()
