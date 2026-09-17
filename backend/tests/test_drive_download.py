import io
import unittest
from unittest.mock import MagicMock, patch

from agent.errors import DriveAPIError
from services.drive import download_drive_folder_archive, download_drive_pdf


ITEM_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"


class FakeDownloadResponse(io.BytesIO):
    def __init__(
        self,
        data: bytes,
        headers: dict[str, str] | None = None,
        *,
        status: int = 200,
    ):
        super().__init__(data)
        self.headers = headers or {}
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DriveDownloadTests(unittest.TestCase):
    @patch("services.drive._drive_api")
    def test_downloads_native_recursive_folder_archive(self, drive_api_context):
        drive_api = MagicMock()
        drive_api_context.return_value.__enter__.return_value = drive_api
        drive_api.api_v1_0_items_export_retrieve_without_preload_content.return_value = FakeDownloadResponse(
            b"PK\x03\x04zip-data", {"Content-Length": "12"}
        )

        result = download_drive_folder_archive(
            "http://drive:8071", "session-secret", ITEM_ID, max_bytes=100
        )

        requested_id = (
            drive_api.api_v1_0_items_export_retrieve_without_preload_content
            .call_args.args[0]
        )
        self.assertEqual(str(requested_id), ITEM_ID)
        self.assertEqual(result, b"PK\x03\x04zip-data")

    @patch("services.drive._drive_api")
    def test_downloads_pdf_with_authenticated_drive_request(self, drive_api_context):
        drive_api = MagicMock()
        drive_api_context.return_value.__enter__.return_value = drive_api
        drive_api.api_v1_0_items_download_retrieve_without_preload_content.return_value = FakeDownloadResponse(
            b"%PDF-test", {"Content-Length": "9"}
        )

        result = download_drive_pdf(
            "http://drive:8071", "session-secret", ITEM_ID, max_bytes=100
        )

        requested_id = (
            drive_api.api_v1_0_items_download_retrieve_without_preload_content
            .call_args.args[0]
        )
        self.assertEqual(str(requested_id), ITEM_ID)
        self.assertEqual(result, b"%PDF-test")

    def test_rejects_non_uuid_item_id_before_network_access(self):
        with self.assertRaisesRegex(DriveAPIError, "item_id must be a valid UUID"):
            download_drive_pdf("http://drive:8071", "session-secret", "not-an-id")

    @patch("services.drive._drive_api")
    def test_rejects_non_pdf_content(self, drive_api_context):
        drive_api = MagicMock()
        drive_api_context.return_value.__enter__.return_value = drive_api
        drive_api.api_v1_0_items_download_retrieve_without_preload_content.return_value = FakeDownloadResponse(
            b"<html>login</html>"
        )

        with self.assertRaisesRegex(DriveAPIError, "not a valid PDF"):
            download_drive_pdf("http://drive:8071", "session-secret", ITEM_ID)

    @patch("services.drive.urlopen")
    @patch("services.drive._drive_api")
    def test_keeps_cookie_for_redirect_on_same_hostname(
        self, drive_api_context, urlopen
    ):
        drive_api = MagicMock()
        drive_api_context.return_value.__enter__.return_value = drive_api
        drive_api.api_v1_0_items_download_retrieve_without_preload_content.return_value = FakeDownloadResponse(
            b"",
            {"Location": "http://drive:8083/media/document.pdf"},
            status=302,
        )
        urlopen.return_value = FakeDownloadResponse(b"%PDF-test")

        download_drive_pdf("http://drive:8071", "session-secret", ITEM_ID)

        redirected_request = urlopen.call_args.args[0]
        self.assertEqual(
            redirected_request.get_header("Cookie"),
            "drive_sessionid=session-secret",
        )
        self.assertIsNone(redirected_request.get_header("Accept"))


if __name__ == "__main__":
    unittest.main()
