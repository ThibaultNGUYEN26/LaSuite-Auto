"""Create a UTF-8 text file in La Suite Drive."""

from __future__ import annotations

import mimetypes
import re
from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import create_drive_file, resolve_drive_upload_acl


EXTENSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,15}$")


class DriveCreateFileAgent(SpecialistAgent):
    name = "drive_create_file"
    description = (
        "Create and upload a new UTF-8 text file with a specific extension in "
        "La Suite Drive. Use only when the user explicitly asks to create a Drive "
        "file. Omit parent_id for My Files, or use a folder UUID returned by "
        "drive_list_items to create it inside that folder. This does not create "
        "binary formats such as real PDF or DOCX documents."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "File name without its final extension.",
            },
            "extension": {
                "type": "string",
                "description": "Requested text-file extension, with or without a dot.",
            },
            "content": {
                "type": "string",
                "description": "UTF-8 text content to upload into the new file.",
            },
            "parent_id": {
                "type": "string",
                "description": (
                    "Optional UUID of an existing Drive folder. Omit it to create "
                    "the file at the top of My Files."
                ),
            },
        },
        "required": ["file_name", "extension", "content"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        base_url: str,
        session_id: str | None,
        *,
        csrf_token: str | None = None,
        upload_acl: str | None = None,
        max_create_bytes: int = 1024 * 1024,
    ) -> None:
        self.base_url = base_url
        self.session_id = session_id or ""
        self.csrf_token = csrf_token
        self.upload_acl = upload_acl
        self.max_create_bytes = max_create_bytes

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        for key in ("file_name", "extension", "content"):
            if not isinstance(arguments.get(key), str):
                raise DriveAPIError(f"{key} must be a string")
        parent_id = arguments.get("parent_id")
        if parent_id is not None and not isinstance(parent_id, str):
            raise DriveAPIError("parent_id must be a string")

        file_name = arguments["file_name"].strip()
        extension = arguments["extension"].strip().removeprefix(".")
        if (
            not file_name
            or file_name in {".", ".."}
            or Path(file_name).name != file_name
            or any(character in file_name for character in '<>:"/\\|?*')
            or file_name.endswith((" ", "."))
        ):
            raise DriveAPIError("file_name contains invalid characters")
        if not EXTENSION_PATTERN.fullmatch(extension):
            raise DriveAPIError("extension must contain only letters, numbers, _ or -")

        data = arguments["content"].encode("utf-8")
        if len(data) > self.max_create_bytes:
            raise DriveAPIError(
                f"File content exceeds the configured {self.max_create_bytes}-byte "
                "creation limit"
            )
        filename = f"{file_name}.{extension}"
        content_type = mimetypes.guess_type(filename)[0] or "text/plain"
        upload_acl = resolve_drive_upload_acl(self.base_url, self.upload_acl)
        return create_drive_file(
            self.base_url,
            self.session_id,
            filename=filename,
            data=data,
            parent_id=parent_id,
            csrf_token=self.csrf_token,
            upload_acl=upload_acl,
            content_type=content_type,
        )
