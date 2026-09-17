import io
import json
import unittest
from unittest.mock import MagicMock, patch

from agent.base import DelegationContext
from agent.errors import DriveAPIError
from agent.specialists.drive import DriveCreateFolderAgent
from services.drive import create_drive_folder


PARENT_ID = "b1f2a5f4-c55a-4a80-939a-5078e5b43a11"
FOLDER_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"


class FakeResponse(io.BytesIO):
    status = 201
    headers: dict[str, str] = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DriveCreateFolderServiceTests(unittest.TestCase):
    @patch("services.drive.GeneratedDriveApi")
    @patch("services.drive.openapi_client.ApiClient")
    def test_creates_top_level_folder(self, api_client_class, api_class):
        api_client_class.return_value.__enter__.return_value = MagicMock()
        api = api_class.return_value
        api.api_v1_0_items_create_without_preload_content.return_value = FakeResponse(
            json.dumps(
                {
                    "id": FOLDER_ID,
                    "title": "Client 1",
                    "url_permalink": "http://drive/explorer/items/client-1",
                }
            ).encode("utf-8")
        )

        result = create_drive_folder(
            "http://drive:8071",
            "session-secret",
            title="Client 1",
            csrf_token="csrf-secret",
        )

        request_model = (
            api.api_v1_0_items_create_without_preload_content.call_args.args[0]
        )
        self.assertEqual(request_model.title, "Client 1")
        self.assertEqual(request_model.type.value, "folder")
        self.assertEqual(
            api.api_v1_0_items_create_without_preload_content.call_args.kwargs[
                "_headers"
            ],
            {"X-CSRFToken": "csrf-secret"},
        )
        self.assertEqual(result["artifact"]["kind"], "folder")
        self.assertEqual(result["artifact"]["reference"], FOLDER_ID)

    @patch("services.drive.GeneratedDriveApi")
    @patch("services.drive.openapi_client.ApiClient")
    def test_creates_nested_folder(self, api_client_class, api_class):
        api_client_class.return_value.__enter__.return_value = MagicMock()
        api = api_class.return_value
        api.api_v1_0_items_children_create_without_preload_content.return_value = (
            FakeResponse(
                json.dumps({"id": FOLDER_ID, "title": "Reports"}).encode("utf-8")
            )
        )

        result = create_drive_folder(
            "http://drive:8071",
            "session-secret",
            title="Reports",
            parent_id=PARENT_ID,
        )

        parent_uuid, request_model = (
            api.api_v1_0_items_children_create_without_preload_content.call_args.args
        )
        self.assertEqual(str(parent_uuid), PARENT_ID)
        self.assertEqual(request_model.title, "Reports")
        self.assertEqual(result["parent_id"], PARENT_ID)

    def test_rejects_invalid_parent_before_request(self):
        with self.assertRaisesRegex(DriveAPIError, "parent_id must be a valid UUID"):
            create_drive_folder(
                "http://drive:8071",
                "session-secret",
                title="Reports",
                parent_id="not-a-uuid",
            )


class DriveCreateFolderAgentTests(unittest.TestCase):
    @patch("agent.specialists.drive.create_folder.create_drive_folder")
    def test_delegates_and_returns_reusable_folder(self, create_folder):
        create_folder.return_value = {
            "status": "created",
            "id": FOLDER_ID,
            "artifact": {
                "kind": "folder",
                "location": "drive",
                "reference": FOLDER_ID,
                "media_type": "inode/directory",
                "name": "Reports",
                "metadata": {},
            },
        }
        agent = DriveCreateFolderAgent(
            "http://drive:8071",
            "session-secret",
            csrf_token="csrf-secret",
        )

        result = agent.execute(
            {"title": "Reports", "parent_id": PARENT_ID},
            DelegationContext(conversation=()),
        )

        self.assertEqual(result["artifact"]["kind"], "folder")
        self.assertEqual(create_folder.call_args.kwargs["parent_id"], PARENT_ID)


if __name__ == "__main__":
    unittest.main()
