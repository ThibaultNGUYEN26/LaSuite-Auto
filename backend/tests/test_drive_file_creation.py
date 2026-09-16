import io
import json
import unittest
from unittest.mock import patch

from agent.base import DelegationContext
from agent.errors import DriveAPIError
from agent.specialists.drive import DriveCreateFileAgent
from services.drive import create_drive_file


ITEM_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"


class FakeResponse(io.BytesIO):
    def __init__(self, payload: dict | None = None):
        super().__init__(json.dumps(payload or {}).encode("utf-8"))
        self.headers = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DriveFileCreationTests(unittest.TestCase):
    @patch("services.drive.urlopen")
    def test_creates_uploads_and_finalizes_file(self, urlopen):
        urlopen.side_effect = [
            FakeResponse(
                {
                    "id": ITEM_ID,
                    "title": "notes",
                    "filename": "notes.md",
                    "policy": "http://storage:9000/upload/signed",
                    "url_permalink": "http://drive/items/notes",
                }
            ),
            FakeResponse(),
            FakeResponse({"id": ITEM_ID}),
        ]

        result = create_drive_file(
            "http://drive:8071",
            "session-secret",
            filename="notes.md",
            data=b"hello",
            csrf_token="csrf-secret",
            upload_acl="private",
            content_type="text/markdown",
        )

        create_request = urlopen.call_args_list[0].args[0]
        self.assertEqual(create_request.get_method(), "POST")
        self.assertEqual(
            json.loads(create_request.data),
            {"type": "file", "filename": "notes.md"},
        )
        self.assertIn("drive_sessionid=session-secret", create_request.get_header("Cookie"))
        self.assertIn("csrftoken=csrf-secret", create_request.get_header("Cookie"))
        self.assertEqual(create_request.get_header("X-csrftoken"), "csrf-secret")

        upload_request = urlopen.call_args_list[1].args[0]
        self.assertEqual(upload_request.get_method(), "PUT")
        self.assertEqual(upload_request.data, b"hello")
        self.assertEqual(upload_request.get_header("Content-type"), "text/markdown")
        self.assertEqual(upload_request.get_header("X-amz-acl"), "private")
        self.assertIsNone(upload_request.get_header("Cookie"))

        finalize_request = urlopen.call_args_list[2].args[0]
        self.assertEqual(finalize_request.get_method(), "POST")
        self.assertTrue(finalize_request.full_url.endswith(f"/{ITEM_ID}/upload-ended/"))
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["bytes_written"], 5)

    @patch("agent.specialists.drive.create_file.create_drive_file")
    def test_agent_builds_filename_and_utf8_content(self, create_file):
        create_file.return_value = {"status": "created"}
        agent = DriveCreateFileAgent(
            "http://drive:8071",
            "session",
            upload_acl="default",
            max_create_bytes=100,
        )

        result = agent.execute(
            {"file_name": "résumé", "extension": ".md", "content": "été"},
            DelegationContext(conversation=()),
        )

        self.assertEqual(result, {"status": "created"})
        self.assertEqual(create_file.call_args.kwargs["filename"], "résumé.md")
        self.assertEqual(create_file.call_args.kwargs["data"], "été".encode("utf-8"))
        self.assertIsNone(create_file.call_args.kwargs["upload_acl"])

    @patch("agent.specialists.drive.create_file.create_drive_file")
    @patch("agent.specialists.drive.create_file.resolve_drive_upload_acl")
    def test_agent_uses_drive_upload_acl(self, resolve_acl, create_file):
        resolve_acl.return_value = "private"
        create_file.return_value = {"status": "created"}
        agent = DriveCreateFileAgent("http://drive:8071", "session")

        agent.execute(
            {"file_name": "notes", "extension": "txt", "content": "hello"},
            DelegationContext(conversation=()),
        )

        self.assertEqual(create_file.call_args.kwargs["upload_acl"], "private")

    def test_agent_rejects_path_in_filename(self):
        agent = DriveCreateFileAgent(
            "http://drive:8071", "session", upload_acl="default"
        )
        with self.assertRaisesRegex(DriveAPIError, "invalid characters"):
            agent.execute(
                {"file_name": "../notes", "extension": "txt", "content": "no"},
                DelegationContext(conversation=()),
            )


if __name__ == "__main__":
    unittest.main()
