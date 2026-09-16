import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fpdf import FPDF

from agent.base import DelegationContext
from agent.specialists.drive.search_pdfs import DriveSearchPdfsAgent
from agent.specialists.local_files.search_pdfs import LocalFilesSearchPdfsAgent
from services.pdf_search import PdfSource, pdf_page_cache, search_pdf_sources


def pdf_bytes(*pages: str) -> bytes:
    pdf = FPDF()
    pdf.set_font("Helvetica", size=12)
    for page in pages:
        pdf.add_page()
        pdf.multi_cell(0, 8, page)
    return bytes(pdf.output())


class PdfCorpusSearchTests(unittest.TestCase):
    def setUp(self):
        pdf_page_cache.clear()

    def test_finds_the_relevant_document_and_page(self):
        sources = [
            PdfSource(
                cache_key="gardening-v1",
                name="gardening.pdf",
                reference="gardening.pdf",
                load=lambda: pdf_bytes("Tomatoes need regular watering."),
            ),
            PdfSource(
                cache_key="linux-v1",
                name="mx-linux.pdf",
                reference="mx-linux.pdf",
                load=lambda: pdf_bytes(
                    "Installation and boot options.",
                    "For multimedia video playback, use VLC media player.",
                ),
            ),
        ]

        result = search_pdf_sources(
            sources,
            query="Which multimedia video player should I use?",
        )

        self.assertEqual(result["documents_scanned"], 2)
        self.assertEqual(result["matches"][0]["source_name"], "mx-linux.pdf")
        self.assertEqual(result["matches"][0]["page"], 2)
        self.assertEqual(result["matches"][0]["citation"], "[mx-linux.pdf, p. 2]")
        self.assertIn("VLC", result["matches"][0]["excerpt"])

    def test_reuses_cached_pages_on_the_next_question(self):
        calls = 0

        def load_pdf():
            nonlocal calls
            calls += 1
            return pdf_bytes("VLC is the recommended video player.")

        source = PdfSource(
            cache_key="manual-version-1",
            name="manual.pdf",
            reference="manual.pdf",
            load=load_pdf,
        )

        search_pdf_sources([source], query="video player")
        search_pdf_sources([source], query="VLC")

        self.assertEqual(calls, 1)

    def test_ranks_real_content_above_a_table_of_contents(self):
        source = PdfSource(
            cache_key="toc-manual-v1",
            name="manual.pdf",
            reference="manual.pdf",
            load=lambda: pdf_bytes(
                "Multimedia ........ 108\nMusic ........ 108\nVideo ........ 109",
                "For multimedia video playback, VLC supports many formats.",
            ),
        )

        result = search_pdf_sources([source], query="multimedia video player")

        self.assertEqual(result["matches"][0]["page"], 2)
        self.assertIn("VLC", result["matches"][0]["excerpt"])


class LocalPdfSearchAgentTests(unittest.TestCase):
    def setUp(self):
        pdf_page_cache.clear()

    def test_searches_all_pdfs_below_a_local_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloads = root / "Downloads"
            downloads.mkdir()
            (downloads / "cooking.pdf").write_bytes(
                pdf_bytes("Bake bread at 220 degrees.")
            )
            (downloads / "manual.pdf").write_bytes(
                pdf_bytes("Use Audacious for music playback.")
            )
            agent = LocalFilesSearchPdfsAgent(
                root,
                max_read_bytes=1_000_000,
            )

            result = agent.execute(
                {"directory": "Downloads", "query": "music playback"},
                DelegationContext(conversation=()),
            )

        self.assertEqual(result["pdfs_discovered"], 2)
        self.assertEqual(result["matches"][0]["source_name"], "manual.pdf")
        self.assertIn("Audacious", result["matches"][0]["excerpt"])

    def test_can_search_only_paths_selected_from_pdf_memories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "manual.pdf").write_bytes(pdf_bytes("Use VLC for video."))
            (root / "unrelated.pdf").write_bytes(pdf_bytes("Gardening advice."))
            agent = LocalFilesSearchPdfsAgent(root, max_read_bytes=1_000_000)

            result = agent.execute(
                {
                    "query": "video player",
                    "relative_paths": ["manual.pdf"],
                },
                DelegationContext(conversation=()),
            )

        self.assertEqual(result["pdfs_discovered"], 1)
        self.assertEqual(result["documents_scanned"], 1)
        self.assertEqual(result["matches"][0]["source_name"], "manual.pdf")


class DrivePdfSearchAgentTests(unittest.TestCase):
    def setUp(self):
        pdf_page_cache.clear()

    @patch("agent.specialists.drive.search_pdfs.download_drive_pdf")
    @patch("agent.specialists.drive.search_pdfs.list_drive_items")
    def test_searches_pdf_contents_from_drive(self, list_items, download_pdf):
        list_items.return_value = {
            "items": [
                {
                    "id": "document-1",
                    "type": "file",
                    "filename": "policy.pdf",
                    "mimetype": "application/pdf",
                    "updated_at": "2026-01-01",
                    "size": 200,
                },
                {
                    "id": "document-2",
                    "type": "file",
                    "filename": "manual.pdf",
                    "mimetype": "application/pdf",
                    "updated_at": "2026-01-01",
                    "size": 200,
                },
            ],
            "complete": True,
        }
        contents = {
            "document-1": pdf_bytes("Annual leave policy."),
            "document-2": pdf_bytes("Use VLC for multimedia video playback."),
        }
        download_pdf.side_effect = lambda base_url, session_id, item_id, **kwargs: (
            contents[item_id]
        )
        agent = DriveSearchPdfsAgent(
            "http://drive",
            "session",
            max_download_bytes=1_000_000,
        )

        result = agent.execute(
            {"query": "multimedia video player"},
            DelegationContext(conversation=()),
        )

        self.assertEqual(result["pdfs_discovered"], 2)
        self.assertEqual(result["matches"][0]["source_name"], "manual.pdf")
        self.assertEqual(download_pdf.call_count, 2)


if __name__ == "__main__":
    unittest.main()
