import tempfile
import unittest
from pathlib import Path

from agent.base import DelegationContext
from agent.errors import LocalFilesError
from agent.specialists.local_files import LocalFilesCreateFileAgent
from services.local_files import create_local_text_file


class LocalFileCreationTests(unittest.TestCase):
    def test_creates_utf8_file_with_requested_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / "Documents"
            documents.mkdir()

            result = create_local_text_file(
                root,
                directory="Documents",
                file_name="meeting-notes",
                extension=".md",
                content="Résumé de la réunion",
                max_bytes=1000,
            )

            target = documents / "meeting-notes.md"
            self.assertEqual(target.read_text(encoding="utf-8"), "Résumé de la réunion")
            self.assertEqual(result["relative_path"], "Documents/meeting-notes.md")
            self.assertEqual(result["extension"], ".md")
            self.assertEqual(result["artifact"]["location"], "local")
            self.assertEqual(
                result["artifact"]["reference"], "Documents/meeting-notes.md"
            )

    def test_never_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "notes.txt"
            target.write_text("keep me", encoding="utf-8")

            with self.assertRaisesRegex(LocalFilesError, "already exists"):
                create_local_text_file(
                    root,
                    directory=".",
                    file_name="notes",
                    extension="txt",
                    content="replacement",
                    max_bytes=1000,
                )

            self.assertEqual(target.read_text(encoding="utf-8"), "keep me")

    def test_rejects_path_characters_in_file_name(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(LocalFilesError, "invalid characters"):
                create_local_text_file(
                    Path(directory),
                    directory=".",
                    file_name="../outside",
                    extension="txt",
                    content="no",
                    max_bytes=1000,
                )

    def test_agent_requires_string_arguments(self):
        agent = LocalFilesCreateFileAgent(Path("."))

        with self.assertRaisesRegex(LocalFilesError, "content must be a string"):
            agent.execute(
                {
                    "directory": ".",
                    "file_name": "notes",
                    "extension": "txt",
                    "content": None,
                },
                DelegationContext(conversation=()),
            )


if __name__ == "__main__":
    unittest.main()
