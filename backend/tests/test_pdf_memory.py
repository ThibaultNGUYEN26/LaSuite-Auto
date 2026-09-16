import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from fpdf import FPDF

from agent.base import DelegationContext
from agent.registry import AgentRegistry
from agent.specialists.local_files.search_pdf_memory import (
    LocalFilesSearchPdfMemoryAgent,
)
from agent.specialists.local_files.summarize_pdf import (
    LocalFilesSummarizePdfAgent,
)
from agent.specialists.local_files.summarize_pdfs import (
    LocalFilesSummarizePdfsAgent,
)
from agent.errors import PdfError
from services.pdf_memory import save_pdf_memory


def pdf_bytes(*pages: str) -> bytes:
    pdf = FPDF()
    pdf.set_font("Helvetica", size=12)
    for page in pages:
        pdf.add_page()
        pdf.multi_cell(0, 8, page)
    return bytes(pdf.output())


class FakeSummaryClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    async def chat_completion_stream(self, **request):
        self.requests.append(deepcopy(request))
        yield {"type": "content", "delta": next(self.responses)}
        yield {"type": "done", "tool_calls": []}


class PdfMemoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_analyzes_every_page_and_creates_a_linked_markdown_memory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloads = root / "Downloads"
            downloads.mkdir()
            source = downloads / "MX Linux Guide.pdf"
            source.write_bytes(
                pdf_bytes(
                    "Installation instructions and system requirements.",
                    "Use VLC for video and Strawberry for music.",
                )
            )
            client = FakeSummaryClient(
                [
                    "## Topics\n- Installation [p. 1]\n- Multimedia [p. 2]",
                    json.dumps(
                        {
                            "title": "MX Linux User Guide",
                            "markdown": (
                                "## Overview\nA practical MX Linux guide. [p. 1]\n\n"
                                "## Key points\nUse VLC for video. [p. 2]\n\n"
                                "## Detailed topic and page guide\n- Installation: p. 1\n"
                                "- Multimedia: p. 2\n\n"
                                "## Questions this document can answer\n"
                                "- Which video player should I use?\n\n"
                                "## Limitations\nSelectable text only."
                            ),
                        }
                    ),
                ]
            )
            agent = LocalFilesSummarizePdfAgent(
                root,
                api_key=None,
                base_url="http://albert",
                requested_model=None,
                max_read_bytes=1_000_000,
                max_pages=100,
                client=client,
                model="text-model",
            )
            registry = AgentRegistry([agent])

            result = await registry.dispatch_async(
                "local_files_summarize_pdf",
                json.dumps({"relative_path": "Downloads/MX Linux Guide.pdf"}),
                DelegationContext(conversation=()),
            )

            target = next((root / "memory").glob("*.md"))
            content = target.read_text(encoding="utf-8")
            self.assertEqual(result["status"], "analyzed")
            self.assertEqual(result["pages_analyzed"], 2)
            self.assertTrue(result["complete"])
            self.assertTrue(result["ready_for_follow_up"])
            self.assertEqual(result["title"], "MX Linux User Guide")
            self.assertNotIn("relative_path", result)
            self.assertNotIn("artifact", result)
            self.assertIn("Use VLC for video", result["analysis"])
            self.assertEqual(target.name, "mx-linux-user-guide.md")
            self.assertIn(
                "[Open the original PDF](<../Downloads/MX%20Linux%20Guide.pdf>)",
                content,
            )
            self.assertIn('"source_path": "Downloads/MX Linux Guide.pdf"', content)
            self.assertIn("Multimedia: p. 2", content)
            self.assertIn("## Page 1", client.requests[0]["messages"][1]["content"])
            self.assertIn("## Page 2", client.requests[0]["messages"][1]["content"])

            memory_search = LocalFilesSearchPdfMemoryAgent(root)
            matches = memory_search.execute(
                {"query": "Which multimedia video player should I use?"},
                DelegationContext(conversation=()),
            )
            self.assertEqual(matches["count"], 1)
            self.assertEqual(
                matches["matches"][0]["source_relative_path"],
                "Downloads/MX Linux Guide.pdf",
            )

    async def test_refreshes_the_same_managed_memory_instead_of_duplicating_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.pdf").write_bytes(pdf_bytes("First version."))
            responses = [
                "Notes [p. 1]",
                '{"title":"Useful Guide","markdown":"## Overview\nFirst [p. 1]"}',
                "Updated notes [p. 1]",
                '{"title":"Better Guide","markdown":"## Overview\nUpdated [p. 1]"}',
            ]
            agent = LocalFilesSummarizePdfAgent(
                root,
                api_key=None,
                base_url="http://albert",
                requested_model=None,
                max_read_bytes=1_000_000,
                max_pages=100,
                client=FakeSummaryClient(responses),
                model="text-model",
            )

            first = await agent.summarize("guide.pdf")
            second = await agent.summarize("guide.pdf")

            self.assertEqual(first["status"], "created")
            self.assertEqual(second["status"], "updated")
            self.assertEqual(first["relative_path"], second["relative_path"])
            self.assertEqual(len(list((root / "memory").glob("*.md"))), 1)
            self.assertIn(
                "Updated [p. 1]",
                (root / second["relative_path"]).read_text(encoding="utf-8"),
            )


class FakeBatchSummarizer:
    def __init__(self, *, failing_path: str | None = None):
        self.failing_path = failing_path
        self.calls = []

    async def summarize(self, relative_path: str):
        self.calls.append(relative_path)
        if relative_path == self.failing_path:
            raise PdfError("Unreadable PDF")
        return {
            "status": "created",
            "source_relative_path": relative_path,
            "relative_path": f"memory/{Path(relative_path).stem}.md",
            "title": Path(relative_path).stem,
        }


class PdfMemoryBatchTests(unittest.IsolatedAsyncioTestCase):
    async def test_skips_fresh_memories_and_isolates_file_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloads = root / "Downloads"
            downloads.mkdir()
            for name in ("fresh.pdf", "new.pdf", "broken.pdf"):
                (downloads / name).write_bytes(b"%PDF-fake")
            save_pdf_memory(
                root,
                source_relative_path="Downloads/fresh.pdf",
                title="Fresh document",
                summary_markdown="## Overview\nAlready summarized.",
                total_pages=1,
            )
            summarizer = FakeBatchSummarizer(
                failing_path="Downloads/broken.pdf"
            )
            agent = LocalFilesSummarizePdfsAgent(
                root,
                summarizer,
                max_files=10,
                concurrency=2,
            )

            result = await agent.execute(
                {
                    "relative_paths": [
                        "Downloads/fresh.pdf",
                        "Downloads/new.pdf",
                        "Downloads/broken.pdf",
                    ]
                },
                DelegationContext(conversation=()),
            )

        self.assertEqual(result["requested"], 3)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["skipped"], 1)
        self.assertEqual(result["failed"], 1)
        self.assertNotIn("Downloads/fresh.pdf", summarizer.calls)
        self.assertIn("Downloads/new.pdf", summarizer.calls)
        self.assertIn("Downloads/broken.pdf", summarizer.calls)

    async def test_discovers_a_bounded_folder_batch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloads = root / "Downloads"
            downloads.mkdir()
            for name in ("one.pdf", "two.pdf", "three.pdf"):
                (downloads / name).write_bytes(b"%PDF-fake")
            summarizer = FakeBatchSummarizer()
            agent = LocalFilesSummarizePdfsAgent(
                root,
                summarizer,
                max_files=2,
                concurrency=1,
            )

            result = await agent.execute(
                {"directory": "Downloads"},
                DelegationContext(conversation=()),
            )

        self.assertEqual(result["requested"], 2)
        self.assertEqual(result["created"], 2)
        self.assertTrue(result["limited"])
        self.assertEqual(len(summarizer.calls), 2)

    async def test_discovers_pdfs_from_several_folders_in_one_batch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder, filename in (
                ("Auditor", "requirements.pdf"),
                ("Client_1", "client-one.pdf"),
                ("Client_2", "client-two.pdf"),
            ):
                target = root / folder
                target.mkdir()
                (target / filename).write_bytes(b"%PDF-fake")
            summarizer = FakeBatchSummarizer()
            agent = LocalFilesSummarizePdfsAgent(
                root,
                summarizer,
                max_files=10,
                concurrency=2,
            )

            result = await agent.execute(
                {"directories": ["Auditor", "Client_1", "Client_2"]},
                DelegationContext(conversation=()),
            )

        self.assertEqual(result["requested"], 3)
        self.assertEqual(result["created"], 3)
        self.assertCountEqual(
            summarizer.calls,
            [
                "Auditor/requirements.pdf",
                "Client_1/client-one.pdf",
                "Client_2/client-two.pdf",
            ],
        )


if __name__ == "__main__":
    unittest.main()
