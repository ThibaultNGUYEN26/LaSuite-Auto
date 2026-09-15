"""Read a local PDF within the configured local-files root."""

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError
from services.local_files import read_local_pdf
from services.pdf import read_pdf_bytes


class LocalFilesReadPdfAgent(SpecialistAgent):
    name = "local_files_read_pdf"
    description = (
        "Read a PDF stored on this computer under the configured local-files root "
        "(normally the user's home folder). Use the relative_path returned by "
        "local_files_list_items. Do not use this for a file in La Suite Drive."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "relative_path": {
                "type": "string",
                "description": (
                    "Path relative to the configured local-files root, exactly as "
                    "returned by local_files_list_items."
                ),
            }
        },
        "required": ["relative_path"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        root: Path,
        *,
        max_read_bytes: int = 20 * 1024 * 1024,
        max_text_characters: int = 80_000,
    ) -> None:
        self.root = root
        self.max_read_bytes = max_read_bytes
        self.max_text_characters = max_text_characters

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        relative_path = arguments.get("relative_path")
        if not isinstance(relative_path, str):
            raise LocalFilesError("relative_path must be a string")
        pdf_bytes = read_local_pdf(
            self.root,
            relative_path,
            max_bytes=self.max_read_bytes,
        )
        result = read_pdf_bytes(
            pdf_bytes,
            max_characters=self.max_text_characters,
        )
        return {"status": "read", "relative_path": relative_path, **result}
