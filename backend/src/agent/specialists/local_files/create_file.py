"""Create a text file with a user-selected extension."""

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError
from services.local_files import create_local_text_file


class LocalFilesCreateFileAgent(SpecialistAgent):
    name = "local_files_create_file"
    description = (
        "Create a new UTF-8 text file with a specific extension inside the configured "
        "local workspace. Use only when the user explicitly asks to create a file. "
        "This never overwrites an existing file and does not create directories."
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
                "description": "File name without its final extension.",
            },
            "extension": {
                "type": "string",
                "description": "Requested extension, with or without a leading dot.",
            },
            "content": {
                "type": "string",
                "description": "UTF-8 text content to write into the new file.",
            },
        },
        "required": ["directory", "file_name", "extension", "content"],
        "additionalProperties": False,
    }

    def __init__(self, root: Path, *, max_create_bytes: int = 1024 * 1024) -> None:
        self.root = root
        self.max_create_bytes = max_create_bytes

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        values = {
            key: arguments.get(key)
            for key in ("directory", "file_name", "extension", "content")
        }
        for key, value in values.items():
            if not isinstance(value, str):
                raise LocalFilesError(f"{key} must be a string")
        return create_local_text_file(
            self.root,
            directory=values["directory"],
            file_name=values["file_name"],
            extension=values["extension"],
            content=values["content"],
            max_bytes=self.max_create_bytes,
        )
