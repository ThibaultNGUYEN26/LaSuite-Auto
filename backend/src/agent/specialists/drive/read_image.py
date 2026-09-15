"""Analyze an image downloaded from La Suite Drive."""

from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import download_drive_file
from services.image import ImageAnalyzer


class DriveReadImageAgent(SpecialistAgent):
    name = "drive_read_image"
    description = (
        "Inspect or read an image stored in La Suite Drive. Use the item_id returned "
        "by drive_list_items and pass what the user wants to know as question. "
        "Supports PNG, JPEG, GIF, and WebP."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "item_id": {
                "type": "string",
                "format": "uuid",
                "description": "UUID of the image in La Suite Drive.",
            },
            "question": {
                "type": "string",
                "description": "What the user wants to know about the image.",
            },
        },
        "required": ["item_id", "question"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        base_url: str,
        session_id: str | None,
        analyzer: ImageAnalyzer,
        *,
        max_download_bytes: int = 10 * 1024 * 1024,
    ) -> None:
        self.base_url = base_url
        self.session_id = session_id
        self.analyzer = analyzer
        self.max_download_bytes = max_download_bytes

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        item_id = arguments.get("item_id")
        question = arguments.get("question")
        if not isinstance(item_id, str):
            raise DriveAPIError("item_id must be a string")
        if not isinstance(question, str) or not question.strip():
            raise DriveAPIError("question must be a non-empty string")
        image_bytes = download_drive_file(
            self.base_url,
            self.session_id or "",
            item_id,
            max_bytes=self.max_download_bytes,
        )
        return {
            "status": "read",
            "item_id": item_id,
            **self.analyzer.analyze(image_bytes, question),
        }
