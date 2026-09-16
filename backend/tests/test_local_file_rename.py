import tempfile
import unittest
from pathlib import Path

from agent.base import DelegationContext
from agent.errors import LocalFilesError
from agent.specialists.local_files import LocalFilesRenameFileAgent
from services.local_files import rename_local_file


class LocalFileRenameTests(unittest.TestCase):
    def test_renames_file_and_preserves_extension_when_omitted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloads = root / "Downloads"
            downloads.mkdir()
            source = downloads / "old-report.csv"
            source.write_text("name,value\nA,1\n", encoding="utf-8")

            result = rename_local_file(
                root,
                relative_path="Downloads/old-report.csv",
                new_name="pasture-report",
            )

            target = downloads / "pasture-report.csv"
            self.assertFalse(source.exists())
            self.assertEqual(target.read_text(encoding="utf-8"), "name,value\nA,1\n")
            self.assertEqual(result["status"], "renamed")
            self.assertEqual(result["relative_path"], "Downloads/pasture-report.csv")
            self.assertEqual(result["artifact"]["reference"], "Downloads/pasture-report.csv")
            self.assertIn(
                result["artifact"]["media_type"],
                {"text/csv", "application/vnd.ms-excel"},
            )

    def test_allows_an_explicit_new_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes.txt").write_text("hello", encoding="utf-8")

            result = rename_local_file(
                root,
                relative_path="notes.txt",
                new_name="notes.md",
            )

            self.assertEqual(result["relative_path"], "notes.md")
            self.assertTrue((root / "notes.md").exists())

    def test_never_overwrites_an_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            target = root / "target.txt"
            source.write_text("source", encoding="utf-8")
            target.write_text("target", encoding="utf-8")

            with self.assertRaisesRegex(LocalFilesError, "already exists"):
                rename_local_file(
                    root,
                    relative_path="source.txt",
                    new_name="target.txt",
                )

            self.assertEqual(source.read_text(encoding="utf-8"), "source")
            self.assertEqual(target.read_text(encoding="utf-8"), "target")

    def test_rejects_a_new_name_containing_a_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.txt").write_text("source", encoding="utf-8")

            with self.assertRaisesRegex(LocalFilesError, "invalid characters"):
                rename_local_file(
                    root,
                    relative_path="source.txt",
                    new_name="../outside.txt",
                )

    def test_agent_accepts_a_local_file_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "before.pdf").write_bytes(b"%PDF-test")
            agent = LocalFilesRenameFileAgent(root)

            result = agent.execute(
                {
                    "artifact": {
                        "kind": "file",
                        "location": "local",
                        "reference": "before.pdf",
                        "media_type": "application/pdf",
                        "name": "before.pdf",
                        "metadata": {},
                    },
                    "new_name": "after",
                },
                DelegationContext(conversation=()),
            )

            self.assertEqual(result["relative_path"], "after.pdf")
            self.assertEqual(result["artifact"]["media_type"], "application/pdf")


if __name__ == "__main__":
    unittest.main()
