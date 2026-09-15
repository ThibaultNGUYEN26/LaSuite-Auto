"""Read a PDF downloaded from La Suite Drive into backend memory."""

from __future__ import annotations

from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import download_drive_pdf
from services.pdf import read_pdf_bytes


class DriveReadPdfAgent(SpecialistAgent):
    name = "drive_read_pdf"
    description = (
        "Download a PDF from La Suite Drive into backend memory and read its text. "
        "The item_id is the Drive file UUID returned by drive_list_items. This is "
        "read-only and does not save the PDF on disk."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "item_id": {
                "type": "string",
                "format": "uuid",
                "description": "UUID of the PDF file in La Suite Drive.",
            }
        },
        "required": ["item_id"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        base_url: str,
        session_id: str | None,
        *,
        max_download_bytes: int = 20 * 1024 * 1024,
        max_text_characters: int = 80_000,
    ) -> None:
        self.base_url = base_url
        self.session_id = session_id
        self.max_download_bytes = max_download_bytes
        self.max_text_characters = max_text_characters

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        item_id = arguments.get("item_id")
        if not isinstance(item_id, str):
            raise DriveAPIError("item_id must be a string")

        pdf_bytes = download_drive_pdf(
            self.base_url,
            self.session_id or "",
            item_id,
            max_bytes=self.max_download_bytes,
        )
        result = read_pdf_bytes(
            pdf_bytes,
            max_characters=self.max_text_characters,
        )
        return {"status": "read", "item_id": item_id, **result}
