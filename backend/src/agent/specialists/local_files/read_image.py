"""Analyze an image under the configured local-files root."""

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError
from services.image import ImageAnalyzer
from services.local_files import read_local_file


class LocalFilesReadImageAgent(SpecialistAgent):
    name = "local_files_read_image"
    description = (
        "Inspect or read an image stored on this computer under the configured local "
        "workspace. Use the relative_path returned by local_files_list_items and pass "
        "what the user wants to know as question. Supports PNG, JPEG, GIF, and WebP."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "relative_path": {
                "type": "string",
                "description": "Image path returned by local_files_list_items.",
            },
            "question": {
                "type": "string",
                "description": "What the user wants to know about the image.",
            },
        },
        "required": ["relative_path", "question"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        root: Path,
        analyzer: ImageAnalyzer,
        *,
        max_read_bytes: int = 10 * 1024 * 1024,
    ) -> None:
        self.root = root
        self.analyzer = analyzer
        self.max_read_bytes = max_read_bytes

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        relative_path = arguments.get("relative_path")
        question = arguments.get("question")
        if not isinstance(relative_path, str):
            raise LocalFilesError("relative_path must be a string")
        if not isinstance(question, str) or not question.strip():
            raise LocalFilesError("question must be a non-empty string")
        image_bytes = read_local_file(
            self.root,
            relative_path,
            max_bytes=self.max_read_bytes,
        )
        return {
            "status": "read",
            "relative_path": relative_path,
            **self.analyzer.analyze(image_bytes, question),
        }
