import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
from zipfile import ZIP_DEFLATED, ZipFile

from agent.base import DelegationContext
from agent.errors import LocalFilesError
from agent.specialists.drive import DriveDownloadFolderAgent


FOLDER_ID = "b1f2a5f4-c55a-4a80-939a-5078e5b43a11"
FILE_ONE_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"
FILE_TWO_ID = "d49c3a68-d042-459f-8639-9958fc4254b5"


def zip_bytes(entries: dict[str, bytes]) -> bytes:
    output = BytesIO()
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in entries.items():
            archive.writestr(name, data)
    return output.getvalue()


class DriveDownloadFolderAgentTests(unittest.IsolatedAsyncioTestCase):
    def _agent(self, root: Path, **limits):
        return DriveDownloadFolderAgent(
            "http://drive:8071",
            "session-secret",
            root,
            max_file_bytes=limits.get("max_file_bytes", 1_000),
            max_files=limits.get("max_files", 10),
            max_total_bytes=limits.get("max_total_bytes", 2_000),
        )

    @patch("agent.specialists.drive.download_folder.download_drive_folder_archive")
    @patch("agent.specialists.drive.download_folder.get_drive_item")
    async def test_preserves_nested_paths_and_binary_bytes(
        self, get_item, download_archive
    ):
        get_item.return_value = {
            "id": FOLDER_ID,
            "type": "folder",
            "title": "Client 1",
        }
        download_archive.return_value = zip_bytes(
            {
                "report.pdf": b"%PDF-binary",
                "Evidence/photo.png": b"\x89PNG",
                "Empty/": b"",
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Downloads").mkdir()

            result = await self._agent(root).execute(
                {"folder_id": FOLDER_ID, "local_directory": "Downloads"},
                DelegationContext(conversation=()),
            )

            self.assertEqual(
                (root / "Downloads" / "Client 1" / "report.pdf").read_bytes(),
                b"%PDF-binary",
            )
            self.assertEqual(
                (
                    root / "Downloads" / "Client 1" / "Evidence" / "photo.png"
                ).read_bytes(),
                b"\x89PNG",
            )
            self.assertTrue(
                (root / "Downloads" / "Client 1" / "Evidence").is_dir()
            )
            self.assertTrue((root / "Downloads" / "Client 1" / "Empty").is_dir())
        self.assertEqual(result["status"], "downloaded")
        self.assertEqual(result["downloaded"], 2)
        self.assertEqual(result["failed"], 0)
        self.assertTrue(result["complete"])
        self.assertEqual(result["artifact"]["kind"], "folder")

    @patch("agent.specialists.drive.download_folder.download_drive_folder_archive")
    @patch("agent.specialists.drive.download_folder.get_drive_item")
    async def test_reports_limits_without_aborting_the_batch(
        self, get_item, download_archive
    ):
        get_item.return_value = {"type": "folder", "title": "Archive"}
        download_archive.return_value = zip_bytes(
            {"large.bin": b"x" * 500, "small.bin": b"ok"}
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = await self._agent(root, max_file_bytes=100).execute(
                {"folder_id": FOLDER_ID, "local_directory": "."},
                DelegationContext(conversation=()),
            )

        self.assertEqual(result["status"], "partially_downloaded")
        self.assertEqual(result["downloaded"], 1)
        self.assertEqual(result["skipped"], 1)
        self.assertTrue(result["limited"])

    @patch("agent.specialists.drive.download_folder.download_drive_folder_archive")
    @patch("agent.specialists.drive.download_folder.get_drive_item")
    async def test_never_overwrites_an_existing_local_folder(
        self, get_item, download_archive
    ):
        get_item.return_value = {"type": "folder", "title": "Client 1"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Client 1").mkdir()

            with self.assertRaisesRegex(LocalFilesError, "already exists"):
                await self._agent(root).execute(
                    {"folder_id": FOLDER_ID, "local_directory": "."},
                    DelegationContext(conversation=()),
                )

        download_archive.assert_not_called()

    @patch("agent.specialists.drive.download_folder.download_drive_file")
    @patch("agent.specialists.drive.download_folder.list_drive_items")
    @patch("agent.specialists.drive.download_folder.get_drive_item")
    async def test_downloads_my_files_without_a_folder_id(
        self, get_item, list_items, download_file
    ):
        list_items.return_value = {
            "items": [],
            "truncated": False,
            "limitation": None,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = await self._agent(root).execute(
                {"local_directory": "."},
                DelegationContext(conversation=()),
            )

            self.assertTrue((root / "My Drive").is_dir())
        get_item.assert_not_called()
        self.assertEqual(result["destination_relative_path"], "My Drive")


if __name__ == "__main__":
    unittest.main()
