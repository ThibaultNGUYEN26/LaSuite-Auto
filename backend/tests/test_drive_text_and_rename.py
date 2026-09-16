import json
import unittest
from unittest.mock import patch

from agent.base import DelegationContext
from agent.errors import DriveAPIError
from agent.specialists.drive import DriveReadTextAgent, DriveRenameFileAgent
from services.drive import read_drive_text, rename_drive_file


ITEM_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"


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
    @patch("services.drive._read_json")
    def test_renames_drive_title_with_patch_and_preserves_extension(self, read_json):
        read_json.side_effect = [
            {
                "id": ITEM_ID,
                "type": "file",
                "title": "Titi",
                "filename": "Titi.csv",
                "mimetype": "text/csv",
            },
            {
                "id": ITEM_ID,
                "type": "file",
                "title": "pasture-data",
                "filename": "Titi.csv",
                "mimetype": "text/csv",
            },
        ]

        result = rename_drive_file(
            "http://drive:8071",
            "session-secret",
            ITEM_ID,
            new_name="pasture-data.csv",
            csrf_token="csrf-secret",
        )

        get_request = read_json.call_args_list[0].args[0]
        patch_request = read_json.call_args_list[1].args[0]
        self.assertEqual(get_request.get_method(), "GET")
        self.assertEqual(patch_request.get_method(), "PATCH")
        self.assertEqual(json.loads(patch_request.data), {"title": "pasture-data"})
        self.assertIn("drive_sessionid=session-secret", patch_request.get_header("Cookie"))
        self.assertEqual(patch_request.get_header("X-csrftoken"), "csrf-secret")
        self.assertEqual(result["status"], "renamed")
        self.assertEqual(result["title"], "pasture-data")
        self.assertEqual(result["artifact"]["reference"], ITEM_ID)

    @patch("services.drive._read_json")
    def test_rejects_changing_the_file_extension(self, read_json):
        read_json.return_value = {
            "id": ITEM_ID,
            "type": "file",
            "title": "Titi",
            "filename": "Titi.csv",
        }

        with self.assertRaisesRegex(DriveAPIError, "cannot change"):
            rename_drive_file(
                "http://drive:8071",
                "session",
                ITEM_ID,
                new_name="pasture-data.pdf",
                csrf_token="csrf",
            )

        self.assertEqual(read_json.call_count, 1)

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
