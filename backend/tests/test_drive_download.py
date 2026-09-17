import io
import unittest
from urllib.error import HTTPError
from unittest.mock import Mock, patch

from agent.errors import DriveAPIError
from services.drive import download_drive_folder_archive, download_drive_pdf


ITEM_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"


class FakeDownloadResponse(io.BytesIO):
    def __init__(self, data: bytes, headers: dict[str, str] | None = None):
        super().__init__(data)
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DriveDownloadTests(unittest.TestCase):
    @patch("services.drive.urlopen")
    def test_downloads_native_recursive_folder_archive(self, urlopen):
        urlopen.return_value = FakeDownloadResponse(
            b"PK\x03\x04zip-data", {"Content-Length": "12"}
        )

        result = download_drive_folder_archive(
            "http://drive:8071", "session-secret", ITEM_ID, max_bytes=100
        )

        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            f"http://drive:8071/api/v1.0/items/{ITEM_ID}/export/",
        )
        self.assertEqual(request.get_header("Cookie"), "drive_sessionid=session-secret")
        self.assertEqual(result, b"PK\x03\x04zip-data")

    @patch("services.drive.build_opener")
    def test_downloads_pdf_with_authenticated_drive_request(self, build_opener):
        opener = Mock()
        opener.open.return_value = FakeDownloadResponse(
            b"%PDF-test", {"Content-Length": "9"}
        )
        build_opener.return_value = opener

        result = download_drive_pdf(
            "http://drive:8071", "session-secret", ITEM_ID, max_bytes=100
        )

        request = opener.open.call_args.args[0]
        self.assertEqual(
            request.full_url,
            f"http://drive:8071/api/v1.0/items/{ITEM_ID}/download/",
        )
        self.assertEqual(request.get_header("Cookie"), "drive_sessionid=session-secret")
        self.assertEqual(request.get_header("Accept"), "application/json")
        self.assertEqual(result, b"%PDF-test")

    def test_rejects_non_uuid_item_id_before_network_access(self):
        with self.assertRaisesRegex(DriveAPIError, "item_id must be a valid UUID"):
            download_drive_pdf("http://drive:8071", "session-secret", "not-an-id")

    @patch("services.drive.build_opener")
    def test_rejects_non_pdf_content(self, build_opener):
        opener = Mock()
        opener.open.return_value = FakeDownloadResponse(b"<html>login</html>")
        build_opener.return_value = opener

        with self.assertRaisesRegex(DriveAPIError, "not a valid PDF"):
            download_drive_pdf("http://drive:8071", "session-secret", ITEM_ID)

    @patch("services.drive.urlopen")
    @patch("services.drive.build_opener")
    def test_keeps_cookie_for_redirect_on_same_hostname(self, build_opener, urlopen):
        opener = Mock()
        opener.open.side_effect = HTTPError(
            f"http://drive:8071/api/v1.0/items/{ITEM_ID}/download/",
            302,
            "Found",
            {"Location": "http://drive:8083/media/document.pdf"},
            None,
        )
        build_opener.return_value = opener
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
