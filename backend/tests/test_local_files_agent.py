import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent.base import DelegationContext
from agent.errors import LocalFilesError
from agent.specialists.local_files import (
    LocalFilesListItemsAgent,
    LocalFilesReadPdfAgent,
)
from services.local_files import (
    list_local_items,
    resolve_local_directory,
    resolve_local_file,
)


class LocalFilesAgentTests(unittest.TestCase):
    def test_lists_files_recursively_with_relative_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes.txt").write_text("hello", encoding="utf-8")
            reports = root / "Reports"
            reports.mkdir()
            (reports / "budget.pdf").write_bytes(b"%PDF-test")

            result = list_local_items(root)

            paths = {item["relative_path"] for item in result["items"]}
            self.assertEqual(paths, {"notes.txt", "Reports", "Reports/budget.pdf"})
            self.assertEqual(result["root_name"], root.name)

    def test_listing_agent_validates_argument_types(self):
        agent = LocalFilesListItemsAgent(Path("Downloads"))

        with self.assertRaisesRegex(LocalFilesError, "limit must be an integer"):
            agent.execute({"limit": "all"}, DelegationContext(conversation=()))

    def test_lists_a_selected_directory_relative_to_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloads = root / "Downloads"
            downloads.mkdir()
            (downloads / "manual.pdf").write_bytes(b"%PDF-test")

            result = list_local_items(root, directory="Downloads", recursive=False)

            self.assertEqual(result["directory"], "Downloads")
            self.assertEqual(result["items"][0]["relative_path"], "Downloads/manual.pdf")

    def test_deep_folders_return_a_friendly_choice_instead_of_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current = root
            for level in range(7):
                current = current / f"level-{level}"
                current.mkdir()

            result = list_local_items(root, max_depth=99)

            paths = {item["relative_path"] for item in result["items"]}
            self.assertIn("level-0/level-1/level-2/level-3/level-4/level-5", paths)
            self.assertNotIn(
                "level-0/level-1/level-2/level-3/level-4/level-5/level-6",
                paths,
            )
            self.assertFalse(result["complete"])
            self.assertIn("specific folder", result["suggested_question"])
            self.assertNotIn("depth", result["limitation"].lower())

    def test_rejects_paths_outside_the_configured_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "Downloads"
            root.mkdir()

            with self.assertRaisesRegex(LocalFilesError, "escapes"):
                resolve_local_file(root, "../secret.pdf")

            with self.assertRaisesRegex(LocalFilesError, "escapes"):
                resolve_local_directory(root, "../Windows")

    @patch("agent.specialists.local_files.read_pdf.read_pdf_bytes")
    @patch("agent.specialists.local_files.read_pdf.read_local_pdf")
    def test_reads_local_pdf_using_listed_relative_path(self, read_local, read_pdf):
        read_local.return_value = b"%PDF-test"
        read_pdf.return_value = {
            "content": "Local PDF content",
            "total_pages": 2,
            "truncated": False,
        }
        root = Path("Downloads")
        agent = LocalFilesReadPdfAgent(
            root,
            max_read_bytes=1234,
            max_text_characters=5000,
        )

        result = agent.execute(
            {"relative_path": "Reports/budget.pdf"},
            DelegationContext(conversation=()),
        )

        read_local.assert_called_once_with(
            root, "Reports/budget.pdf", max_bytes=1234
        )
        read_pdf.assert_called_once_with(b"%PDF-test", max_characters=5000)
        self.assertEqual(result["content"], "Local PDF content")


if __name__ == "__main__":
    unittest.main()
