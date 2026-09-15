import unittest
from pathlib import Path
from unittest.mock import patch

from agent.base import DelegationContext
from agent.errors import SpecialistAgentError
from agent.specialists.drive.read_image import DriveReadImageAgent
from agent.specialists.local_files.read_image import LocalFilesReadImageAgent
from services.image import detect_image_mime


ITEM_ID = "4d57f9aa-f5b6-4581-af99-28c6f935cd2b"


class FakeImageAnalyzer:
    def __init__(self):
        self.calls = []

    def analyze(self, data: bytes, question: str):
        self.calls.append((data, question))
        return {
            "answer": "The image contains a chart.",
            "mime_type": "image/png",
            "model": "vision-model-id",
        }


class ImageAgentTests(unittest.TestCase):
    def test_detects_supported_image_types(self):
        self.assertEqual(detect_image_mime(b"\x89PNG\r\n\x1a\nrest"), "image/png")
        self.assertEqual(detect_image_mime(b"\xff\xd8\xffrest"), "image/jpeg")
        self.assertEqual(detect_image_mime(b"GIF89arest"), "image/gif")
        self.assertEqual(
            detect_image_mime(b"RIFF\x04\x00\x00\x00WEBPrest"), "image/webp"
        )

    def test_rejects_unsupported_image_data(self):
        with self.assertRaisesRegex(SpecialistAgentError, "Unsupported image format"):
            detect_image_mime(b"not-an-image")

    @patch("agent.specialists.drive.read_image.download_drive_file")
    def test_drive_image_agent_downloads_and_analyzes_image(self, download):
        download.return_value = b"\x89PNG\r\n\x1a\nrest"
        analyzer = FakeImageAnalyzer()
        agent = DriveReadImageAgent(
            "http://drive:8071",
            "session-secret",
            analyzer,
            max_download_bytes=1234,
        )

        result = agent.execute(
            {"item_id": ITEM_ID, "question": "What is shown?"},
            DelegationContext(conversation=()),
        )

        download.assert_called_once_with(
            "http://drive:8071", "session-secret", ITEM_ID, max_bytes=1234
        )
        self.assertEqual(analyzer.calls[0][1], "What is shown?")
        self.assertEqual(result["answer"], "The image contains a chart.")

    @patch("agent.specialists.local_files.read_image.read_local_file")
    def test_local_image_agent_reads_and_analyzes_image(self, read_local):
        read_local.return_value = b"\x89PNG\r\n\x1a\nrest"
        analyzer = FakeImageAnalyzer()
        root = Path("C:/Users/test")
        agent = LocalFilesReadImageAgent(root, analyzer, max_read_bytes=4321)

        result = agent.execute(
            {"relative_path": "Pictures/chart.png", "question": "Read the chart"},
            DelegationContext(conversation=()),
        )

        read_local.assert_called_once_with(
            root, "Pictures/chart.png", max_bytes=4321
        )
        self.assertEqual(result["model"], "vision-model-id")


if __name__ == "__main__":
    unittest.main()
