import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent.base import DelegationContext
from agent.errors import DriveAPIError
from agent.specialists.drive import DriveUploadFileAgent


class DriveUploadFileAgentTests(unittest.TestCase):
    def _agent(self, root: Path, *, max_upload_bytes: int = 1000):
        return DriveUploadFileAgent(
            "http://drive:8071",
            "session-secret",
            root,
            csrf_token="csrf-secret",
            upload_acl="private",
            max_upload_bytes=max_upload_bytes,
        )

    @patch("agent.specialists.drive.upload_file.resolve_drive_upload_acl")
    @patch("agent.specialists.drive.upload_file.create_drive_file")
    def test_uploads_pdf_without_changing_bytes(self, create_file, resolve_acl):
        resolve_acl.return_value = "private"
        create_file.return_value = {
            "status": "created",
            "id": "4d57f9aa-f5b6-4581-af99-28c6f935cd2b",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloads = root / "Downloads"
            downloads.mkdir()
            pdf_data = b"%PDF-1.7\x00\xffbinary-payload"
            (downloads / "report.pdf").write_bytes(pdf_data)

            result = self._agent(root).execute(
                {
                    "relative_path": "Downloads/report.pdf",
                    "parent_id": "b1f2a5f4-c55a-4a80-939a-5078e5b43a11",
                },
                DelegationContext(conversation=()),
            )

        kwargs = create_file.call_args.kwargs
        self.assertEqual(kwargs["filename"], "report.pdf")
        self.assertEqual(kwargs["data"], pdf_data)
        self.assertEqual(kwargs["content_type"], "application/pdf")
        self.assertEqual(kwargs["upload_acl"], "private")
        self.assertEqual(result["source_relative_path"], "Downloads/report.pdf")

    @patch("agent.specialists.drive.upload_file.resolve_drive_upload_acl")
    @patch("agent.specialists.drive.upload_file.create_drive_file")
    def test_can_rename_binary_at_destination(self, create_file, resolve_acl):
        resolve_acl.return_value = None
        create_file.return_value = {"status": "created"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "archive.bin").write_bytes(b"\x00\x01\x02")

            self._agent(root).execute(
                {
                    "relative_path": "archive.bin",
                    "destination_name": "backup.dat",
                },
                DelegationContext(conversation=()),
            )

        self.assertEqual(create_file.call_args.kwargs["filename"], "backup.dat")
        self.assertEqual(
            create_file.call_args.kwargs["content_type"],
            "application/octet-stream",
        )

    def test_rejects_invalid_destination_name(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "file.bin").write_bytes(b"data")
            with self.assertRaisesRegex(DriveAPIError, "invalid characters"):
                self._agent(root).execute(
                    {
                        "relative_path": "file.bin",
                        "destination_name": "../outside.bin",
                    },
                    DelegationContext(conversation=()),
                )


if __name__ == "__main__":
    unittest.main()
