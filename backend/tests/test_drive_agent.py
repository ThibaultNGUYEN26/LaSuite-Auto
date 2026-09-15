import io
import json
import unittest
from unittest.mock import patch

from agent.base import DelegationContext
from agent.drive import DriveListItemsAgent, list_drive_items
from agent.errors import DriveAPIError


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DriveListItemsAgentTests(unittest.TestCase):
    @patch("agent.drive.urlopen")
    def test_lists_authenticated_items_and_compacts_the_response(self, urlopen):
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
        urlopen.return_value = FakeResponse(json.dumps(payload).encode("utf-8"))

        result = list_drive_items(
            "http://drive:8071", "session-secret", limit=25, recursive=False
        )

        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url, "http://drive:8071/api/v1.0/items/?page_size=25"
        )
        self.assertEqual(request.get_header("Cookie"), "drive_sessionid=session-secret")
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["returned"], 1)
        self.assertNotIn("abilities", result["items"][0])
        self.assertEqual(result["items"][0]["title"], "Reports")
        self.assertEqual(result["items"][0]["path"], ["Reports"])

    @patch("agent.drive.urlopen")
    def test_recursively_lists_folder_children(self, urlopen):
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
        urlopen.side_effect = [
            FakeResponse(json.dumps(root_payload).encode("utf-8")),
            FakeResponse(json.dumps(child_payload).encode("utf-8")),
        ]

        result = list_drive_items("http://drive:8071", "session-secret")

        self.assertEqual(result["returned"], 2)
        self.assertEqual(
            result["items"][1]["path"], ["Reports", "Annual report.pdf"]
        )
        child_request = urlopen.call_args_list[1].args[0]
        self.assertIn(f"/items/{folder_id}/children/", child_request.full_url)

    def test_requires_authentication_instead_of_returning_an_empty_drive(self):
        agent = DriveListItemsAgent("http://drive:8071", None)

        with self.assertRaisesRegex(DriveAPIError, "DRIVE_SESSION_ID"):
            agent.execute({}, DelegationContext(conversation=()))

    def test_rejects_an_invalid_limit(self):
        agent = DriveListItemsAgent("http://drive:8071", "session-secret")

        with self.assertRaisesRegex(DriveAPIError, "limit must be an integer"):
            agent.execute({"limit": "many"}, DelegationContext(conversation=()))


if __name__ == "__main__":
    unittest.main()
