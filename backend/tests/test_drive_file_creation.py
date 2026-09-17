import io
import json
import unittest
from unittest.mock import MagicMock, patch

from agent.base import DelegationContext
from agent.errors import DriveAPIError
from agent.specialists.drive import DriveCreateFileAgent, DriveCreateFilesAgent
from services.drive import create_drive_file


ITEM_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"


class FakeResponse(io.BytesIO):
    def __init__(self, payload: dict | None = None):
        super().__init__(json.dumps(payload or {}).encode("utf-8"))
        self.headers = {}
        self.status = 200

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DriveFileCreationTests(unittest.TestCase):
    @patch("services.drive.urlopen")
    @patch("services.drive._drive_api")
    def test_creates_uploads_and_finalizes_file(self, drive_api_context, urlopen):
        drive_api = MagicMock()
        drive_api_context.return_value.__enter__.return_value = drive_api
        drive_api.api_v1_0_items_create_without_preload_content.return_value = (
            FakeResponse(
                {
                    "id": ITEM_ID,
                    "title": "notes",
                    "filename": "notes.md",
                    "policy": "http://storage:9000/upload/signed",
                    "url_permalink": "http://drive/items/notes",
                }
            )
        )
        drive_api.api_v1_0_items_upload_ended_create_without_preload_content.return_value = (
            FakeResponse({"id": ITEM_ID})
        )
        urlopen.return_value = FakeResponse()

        result = create_drive_file(
            "http://drive:8071",
            "session-secret",
            filename="notes.md",
            data=b"hello",
            csrf_token="csrf-secret",
            upload_acl="private",
            content_type="text/markdown",
        )

        create_model = (
            drive_api.api_v1_0_items_create_without_preload_content.call_args.args[0]
        )
        self.assertEqual(create_model.type.value, "file")
        self.assertEqual(create_model.filename, "notes.md")
        self.assertEqual(
            drive_api.api_v1_0_items_create_without_preload_content.call_args.kwargs[
                "_headers"
            ],
            {"X-CSRFToken": "csrf-secret"},
        )

        upload_request = urlopen.call_args.args[0]
        self.assertEqual(upload_request.get_method(), "PUT")
        self.assertEqual(upload_request.data, b"hello")
        self.assertEqual(upload_request.get_header("Content-type"), "text/markdown")
        self.assertEqual(upload_request.get_header("X-amz-acl"), "private")
        self.assertIsNone(upload_request.get_header("Cookie"))

        finalized_id = (
            drive_api.api_v1_0_items_upload_ended_create_without_preload_content
            .call_args.args[0]
        )
        self.assertEqual(str(finalized_id), ITEM_ID)
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["bytes_written"], 5)
        self.assertEqual(result["artifact"]["location"], "drive")
        self.assertEqual(result["artifact"]["reference"], ITEM_ID)

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

    @patch("agent.specialists.drive.create_file.create_drive_file")
    def test_batch_agent_creates_every_file_in_one_call(self, create_file):
        create_file.side_effect = [
            {
                "status": "created",
                "filename": "random_1.txt",
                "artifact": {"reference": "item-1"},
            },
            {
                "status": "created",
                "filename": "random_2.txt",
                "artifact": {"reference": "item-2"},
            },
        ]
        agent = DriveCreateFilesAgent(
            "http://drive:8071",
            "session",
            upload_acl="default",
        )

        result = agent.execute(
            {
                "files": [
                    {
                        "file_name": "random_1",
                        "extension": "txt",
                        "content": "first",
                    },
                    {
                        "file_name": "random_2",
                        "extension": ".txt",
                        "content": "second",
                    },
                ]
            },
            DelegationContext(conversation=()),
        )

        self.assertEqual(result["status"], "created")
        self.assertEqual(result["requested_count"], 2)
        self.assertEqual(result["created_count"], 2)
        self.assertTrue(result["complete"])
        self.assertEqual(
            result["artifacts"],
            [{"reference": "item-1"}, {"reference": "item-2"}],
        )
        self.assertEqual(create_file.call_count, 2)
        self.assertEqual(
            create_file.call_args_list[0].kwargs["filename"], "random_1.txt"
        )
        self.assertEqual(create_file.call_args_list[1].kwargs["data"], b"second")

    @patch("agent.specialists.drive.create_file.create_drive_file")
    def test_batch_agent_validates_every_file_before_creating_anything(
        self, create_file
    ):
        agent = DriveCreateFilesAgent(
            "http://drive:8071",
            "session",
            upload_acl="default",
        )

        with self.assertRaisesRegex(DriveAPIError, "File 2 is invalid"):
            agent.execute(
                {
                    "files": [
                        {
                            "file_name": "valid",
                            "extension": "txt",
                            "content": "safe",
                        },
                        {
                            "file_name": "../invalid",
                            "extension": "txt",
                            "content": "unsafe",
                        },
                    ]
                },
                DelegationContext(conversation=()),
            )

        create_file.assert_not_called()

    @patch("agent.specialists.drive.create_file.create_drive_file")
    def test_batch_agent_reports_partial_failures(self, create_file):
        create_file.side_effect = [
            {
                "status": "created",
                "filename": "first.txt",
                "artifact": {"reference": "item-1"},
            },
            DriveAPIError("Drive storage was unavailable"),
        ]
        agent = DriveCreateFilesAgent(
            "http://drive:8071",
            "session",
            upload_acl="default",
        )

        result = agent.execute(
            {
                "files": [
                    {"file_name": "first", "extension": "txt", "content": "1"},
                    {"file_name": "second", "extension": "txt", "content": "2"},
                ]
            },
            DelegationContext(conversation=()),
        )

        self.assertEqual(result["status"], "partially_created")
        self.assertFalse(result["complete"])
        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["failed_count"], 1)
        self.assertEqual(result["failures"][0]["filename"], "second.txt")


if __name__ == "__main__":
    unittest.main()
