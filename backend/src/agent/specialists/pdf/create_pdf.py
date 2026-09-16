"""Create a simple PDF file with a title and plain-text body."""

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import PdfError
from services.pdf import create_local_pdf


class PdfCreateAgent(SpecialistAgent):
    name = "pdf_create"
    description = (
        "Create a new simple PDF file with an optional title and plain-text body "
        "inside the configured local workspace. Use only when the user explicitly "
        "asks to create a PDF. This never overwrites an existing file and does not "
        "create directories. For Markdown content with a header, footer, or page "
        "numbers, use pdf_apply_template instead."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": (
                    "Existing destination directory relative to the local workspace, "
                    "for example Documents or Desktop. Use . for the workspace root."
                ),
            },
            "file_name": {
                "type": "string",
                "description": "File name without the .pdf extension.",
            },
            "title": {
                "type": "string",
                "description": "Optional title rendered at the top of the first page.",
                "default": "",
            },
            "body_text": {
                "type": "string",
                "description": "Plain text content of the PDF.",
            },
        },
        "required": ["directory", "file_name", "body_text"],
        "additionalProperties": False,
    }

    def __init__(self, root: Path, *, max_body_characters: int = 200_000) -> None:
        self.root = root
        self.max_body_characters = max_body_characters

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        for key in ("directory", "file_name", "body_text"):
            if not isinstance(arguments.get(key), str):
                raise PdfError(f"{key} must be a string")
        title = arguments.get("title", "")
        if not isinstance(title, str):
            raise PdfError("title must be a string")
        return create_local_pdf(
            self.root,
            directory=arguments["directory"],
            file_name=arguments["file_name"],
            title=title,
            body_text=arguments["body_text"],
            max_body_characters=self.max_body_characters,
        )
