import tempfile
import unittest
from pathlib import Path

from agent.base import DelegationContext
from agent.errors import LocalFilesError
from agent.specialists.local_files import (
    LocalFilesCreateFileAgent,
    LocalFilesCreateFolderAgent,
    LocalFilesListItemsAgent,
)


class LocalFolderCreationTests(unittest.TestCase):
    def test_creates_folder_then_file_and_searches_inside_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloads = root / "Downloads"
            downloads.mkdir()
            folder_agent = LocalFilesCreateFolderAgent(root)
            file_agent = LocalFilesCreateFileAgent(root)
            list_agent = LocalFilesListItemsAgent(root)
            context = DelegationContext(conversation=())

            folder = folder_agent.execute(
                {"parent_directory": "Downloads", "folder_name": "Client 1"},
                context,
            )
            created_file = file_agent.execute(
                {
                    "directory": folder["relative_path"],
                    "file_name": "audit-notes",
                    "extension": "txt",
                    "content": "Client evidence",
                },
                context,
            )
            listing = list_agent.execute(
                {"directory": folder["relative_path"], "recursive": True},
                context,
            )

            self.assertEqual(folder["relative_path"], "Downloads/Client 1")
            self.assertEqual(folder["artifact"]["kind"], "folder")
            self.assertEqual(
                created_file["relative_path"],
                "Downloads/Client 1/audit-notes.txt",
            )
            self.assertEqual(
                [item["relative_path"] for item in listing["items"]],
                ["Downloads/Client 1/audit-notes.txt"],
            )

    def test_does_not_reuse_an_existing_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Client 1").mkdir()
            agent = LocalFilesCreateFolderAgent(root)

            with self.assertRaisesRegex(LocalFilesError, "already exists"):
                agent.execute(
                    {"parent_directory": ".", "folder_name": "Client 1"},
                    DelegationContext(conversation=()),
                )

    def test_rejects_folder_names_that_escape_the_parent(self):
        with tempfile.TemporaryDirectory() as directory:
            agent = LocalFilesCreateFolderAgent(Path(directory))

            with self.assertRaisesRegex(LocalFilesError, "invalid characters"):
                agent.execute(
                    {"parent_directory": ".", "folder_name": "../outside"},
                    DelegationContext(conversation=()),
                )


if __name__ == "__main__":
    unittest.main()
