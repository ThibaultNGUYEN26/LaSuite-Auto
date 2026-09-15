import unittest
from unittest.mock import patch

from agent.base import DelegationContext
from agent.errors import DriveAPIError
from agent.specialists.drive.read_pdf import DriveReadPdfAgent


ITEM_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"


class DriveReadPdfAgentTests(unittest.TestCase):
    @patch("agent.specialists.drive.read_pdf.read_pdf_bytes")
    @patch("agent.specialists.drive.read_pdf.download_drive_pdf")
    def test_downloads_and_reads_pdf_in_memory(self, download, read_pdf):
        download.return_value = b"%PDF-fake"
        read_pdf.return_value = {
            "content": "The PDF content",
            "total_pages": 8,
            "truncated": False,
        }
        agent = DriveReadPdfAgent(
            "http://drive:8071",
            "session-secret",
            max_download_bytes=1234,
            max_text_characters=5000,
        )

        result = agent.execute(
            {"item_id": ITEM_ID},
            DelegationContext(conversation=()),
        )

        download.assert_called_once_with(
            "http://drive:8071", "session-secret", ITEM_ID, max_bytes=1234
        )
        read_pdf.assert_called_once_with(
            b"%PDF-fake",
            max_characters=5000,
        )
        self.assertEqual(result["status"], "read")
        self.assertEqual(result["content"], "The PDF content")

    def test_requires_an_item_id(self):
        agent = DriveReadPdfAgent("http://drive:8071", "session-secret")

        with self.assertRaisesRegex(DriveAPIError, "item_id must be a string"):
            agent.execute({}, DelegationContext(conversation=()))

if __name__ == "__main__":
    unittest.main()
