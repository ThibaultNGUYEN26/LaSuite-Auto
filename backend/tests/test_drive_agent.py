import io
import json
import unittest
from unittest.mock import MagicMock, patch

from agent.base import DelegationContext
from agent.specialists.drive import DriveListItemsAgent
from agent.errors import DriveAPIError
from services.drive import list_drive_items


class FakeResponse(io.BytesIO):
    status = 200
    headers: dict[str, str] = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DriveListItemsAgentTests(unittest.TestCase):
    @patch("services.drive._drive_api")
    def test_lists_authenticated_items_and_compacts_the_response(self, drive_api_context):
        payload = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "item-1",
                    "title": "Reports",
                    "type": "folder",
                    "filename": None,
                    "mimetype": None,
                    "size": None,
                    "updated_at": "2026-09-15T12:00:00Z",
                    "url_permalink": "http://drive/items/item-1",
                    "abilities": {"update": True},
                }
            ],
        }
        drive_api = MagicMock()
        drive_api_context.return_value.__enter__.return_value = drive_api
        drive_api.api_v1_0_items_list_without_preload_content.return_value = (
            FakeResponse(json.dumps(payload).encode("utf-8"))
        )

        result = list_drive_items(
            "http://drive:8071", "session-secret", limit=25, recursive=False
        )

        self.assertEqual(
            drive_api.api_v1_0_items_list_without_preload_content.call_args.kwargs[
                "page_size"
            ],
            25,
        )
        drive_api_context.assert_called_once_with(
            "http://drive:8071", "session-secret"
        )
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["returned"], 1)
        self.assertNotIn("abilities", result["items"][0])
        self.assertEqual(result["items"][0]["title"], "Reports")
        self.assertEqual(result["items"][0]["path"], ["Reports"])

    @patch("services.drive._drive_api")
    def test_recursively_lists_folder_children(self, drive_api_context):
        folder_id = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"
        root_payload = {
            "count": 1,
            "next": None,
            "results": [{"id": folder_id, "title": "Reports", "type": "folder"}],
        }
        child_payload = {
            "count": 1,
            "next": None,
            "results": [
                {"id": "file-1", "title": "Annual report.pdf", "type": "file"}
            ],
        }
        drive_api = MagicMock()
        drive_api_context.return_value.__enter__.return_value = drive_api
        drive_api.api_v1_0_items_list_without_preload_content.return_value = (
            FakeResponse(json.dumps(root_payload).encode("utf-8"))
        )
        drive_api.api_v1_0_items_children_retrieve_without_preload_content.return_value = (
            FakeResponse(json.dumps(child_payload).encode("utf-8"))
        )

        result = list_drive_items("http://drive:8071", "session-secret")

        self.assertEqual(result["returned"], 2)
        self.assertEqual(
            result["items"][1]["path"], ["Reports", "Annual report.pdf"]
        )
        child_id = (
            drive_api.api_v1_0_items_children_retrieve_without_preload_content
            .call_args.args[0]
        )
        self.assertEqual(str(child_id), folder_id)

    def test_requires_authentication_instead_of_returning_an_empty_drive(self):
        agent = DriveListItemsAgent("http://drive:8071", None)

        with self.assertRaisesRegex(DriveAPIError, "DRIVE_SESSION_ID"):
            agent.execute({}, DelegationContext(conversation=()))

    def test_rejects_an_invalid_limit(self):
        agent = DriveListItemsAgent("http://drive:8071", "session-secret")

        with self.assertRaisesRegex(DriveAPIError, "limit must be an integer"):
            agent.execute({"limit": "many"}, DelegationContext(conversation=()))

    @patch("agent.specialists.drive.list_items.list_drive_items")
    def test_returns_a_concise_direct_overview_for_a_listing_request(
        self, list_items
    ):
        list_items.return_value = {
            "count": 3,
            "top_level_count": 2,
            "recursive": True,
            "limitation": None,
            "items": [
                {
                    "title": "Reports",
                    "type": "folder",
                    "depth": 0,
                    "path": ["Reports"],
                    "url_permalink": "http://drive/items/reports",
                },
                {
                    "title": "Audit.pdf",
                    "type": "file",
                    "depth": 1,
                    "path": ["Reports", "Audit.pdf"],
                },
                {
                    "title": "Notes.txt",
                    "type": "file",
                    "depth": 0,
                    "path": ["Notes.txt"],
                    "url_permalink": "http://drive/items/notes",
                },
            ],
        }
        agent = DriveListItemsAgent("http://drive:8071", "session-secret")

        result = agent.execute(
            {"purpose": "answer_user"}, DelegationContext(conversation=())
        )

        overview = result["_assistant_response"]
        self.assertFalse(list_items.call_args.kwargs["recursive"])
        self.assertIn("**3 items scanned**", overview)
        self.assertIn("[Reports](http://drive/items/reports) — 1 item found inside", overview)
        self.assertIn("[Notes.txt](http://drive/items/notes)", overview)


if __name__ == "__main__":
    unittest.main()
