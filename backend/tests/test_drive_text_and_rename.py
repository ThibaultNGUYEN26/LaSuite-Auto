import io
import json
import unittest
from unittest.mock import MagicMock, patch

from agent.base import DelegationContext
from agent.errors import DriveAPIError
from agent.specialists.drive import DriveReadTextAgent, DriveRenameFileAgent
from services.drive import read_drive_text, rename_drive_file


ITEM_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"


class FakeResponse(io.BytesIO):
    status = 200
    headers: dict[str, str] = {}

    def __init__(self, payload: dict):
        super().__init__(json.dumps(payload).encode("utf-8"))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DriveTextReaderTests(unittest.TestCase):
    @patch("services.drive.download_drive_file")
    def test_reads_utf8_csv_with_bom_and_accents(self, download):
        download.return_value = "année,surface pâturale\n2025,48.7\n".encode(
            "utf-8-sig"
        )

        result = read_drive_text(
            "http://drive:8071",
            "session",
            ITEM_ID,
            filename="pasture.csv",
            max_bytes=1000,
            max_characters=1000,
        )

        self.assertEqual(result["encoding"], "utf-8-sig")
        self.assertIn("surface pâturale", result["content"])
        self.assertNotIn("\ufeff", result["content"])
        self.assertEqual(result["artifact"]["location"], "drive")
        self.assertEqual(result["artifact"]["reference"], ITEM_ID)

    @patch("agent.specialists.drive.read_text.read_drive_text")
    def test_agent_consumes_a_drive_artifact(self, read_text):
        read_text.return_value = {"status": "read", "content": "hello"}
        agent = DriveReadTextAgent("http://drive:8071", "session")

        result = agent.execute(
            {
                "artifact": {
                    "kind": "file",
                    "location": "drive",
                    "reference": ITEM_ID,
                    "media_type": "text/csv",
                    "name": "data.csv",
                    "metadata": {},
                }
            },
            DelegationContext(conversation=()),
        )

        self.assertEqual(result["content"], "hello")
        self.assertEqual(read_text.call_args.args[2], ITEM_ID)
        self.assertEqual(read_text.call_args.kwargs["filename"], "data.csv")


class DriveRenameTests(unittest.TestCase):
    @patch("services.drive._drive_api")
    def test_renames_drive_title_with_patch_and_preserves_extension(
        self, drive_api_context
    ):
        drive_api = MagicMock()
        drive_api_context.return_value.__enter__.return_value = drive_api
        drive_api.api_v1_0_items_retrieve_without_preload_content.return_value = (
            FakeResponse({
                "id": ITEM_ID,
                "type": "file",
                "title": "Titi",
                "filename": "Titi.csv",
                "mimetype": "text/csv",
            })
        )
        drive_api.api_v1_0_items_partial_update_without_preload_content.return_value = (
            FakeResponse({
                "id": ITEM_ID,
                "type": "file",
                "title": "pasture-data",
                "filename": "Titi.csv",
                "mimetype": "text/csv",
            })
        )

        result = rename_drive_file(
            "http://drive:8071",
            "session-secret",
            ITEM_ID,
            new_name="pasture-data.csv",
            csrf_token="csrf-secret",
        )

        patch_model = (
            drive_api.api_v1_0_items_partial_update_without_preload_content
            .call_args.args[1]
        )
        self.assertEqual(patch_model.title, "pasture-data")
        self.assertEqual(
            drive_api.api_v1_0_items_partial_update_without_preload_content
            .call_args.kwargs["_headers"],
            {"X-CSRFToken": "csrf-secret"},
        )
        self.assertEqual(result["status"], "renamed")
        self.assertEqual(result["title"], "pasture-data")
        self.assertEqual(result["artifact"]["reference"], ITEM_ID)

    @patch("services.drive._drive_api")
    def test_rejects_changing_the_file_extension(self, drive_api_context):
        drive_api = MagicMock()
        drive_api_context.return_value.__enter__.return_value = drive_api
        drive_api.api_v1_0_items_retrieve_without_preload_content.return_value = (
            FakeResponse(
                {
                    "id": ITEM_ID,
                    "type": "file",
                    "title": "Titi",
                    "filename": "Titi.csv",
                }
            )
        )

        with self.assertRaisesRegex(DriveAPIError, "cannot change"):
            rename_drive_file(
                "http://drive:8071",
                "session",
                ITEM_ID,
                new_name="pasture-data.pdf",
                csrf_token="csrf",
            )

        drive_api.api_v1_0_items_partial_update_without_preload_content.assert_not_called()

    @patch("agent.specialists.drive.rename_file.rename_drive_file")
    def test_agent_consumes_a_drive_artifact(self, rename):
        rename.return_value = {"status": "renamed", "title": "pasture-data"}
        agent = DriveRenameFileAgent(
            "http://drive:8071",
            "session",
            csrf_token="csrf",
        )

        result = agent.execute(
            {
                "artifact": {
                    "kind": "file",
                    "location": "drive",
                    "reference": ITEM_ID,
                    "media_type": "text/csv",
                    "name": "Titi.csv",
                    "metadata": {},
                },
                "new_name": "pasture-data",
            },
            DelegationContext(conversation=()),
        )

        self.assertEqual(result["status"], "renamed")
        self.assertEqual(rename.call_args.args[2], ITEM_ID)
        self.assertEqual(rename.call_args.kwargs["new_name"], "pasture-data")


if __name__ == "__main__":
    unittest.main()
