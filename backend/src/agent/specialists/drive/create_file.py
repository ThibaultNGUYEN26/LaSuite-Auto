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


def _prepare_text_file(
    arguments: dict[str, Any], *, max_create_bytes: int
) -> tuple[str, bytes, str]:
    """Validate one requested text file before any Drive mutation occurs."""
    for key in ("file_name", "extension", "content"):
        if not isinstance(arguments.get(key), str):
            raise DriveAPIError(f"{key} must be a string")

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
    if len(data) > max_create_bytes:
        raise DriveAPIError(
            f"File content exceeds the configured {max_create_bytes}-byte "
            "creation limit"
        )
    filename = f"{file_name}.{extension}"
    content_type = mimetypes.guess_type(filename)[0] or "text/plain"
    return filename, data, content_type


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
        parent_id = arguments.get("parent_id")
        if parent_id is not None and not isinstance(parent_id, str):
            raise DriveAPIError("parent_id must be a string")
        filename, data, content_type = _prepare_text_file(
            arguments, max_create_bytes=self.max_create_bytes
        )
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


class DriveCreateFilesAgent(SpecialistAgent):
    """Create a bounded batch of text files in one orchestration action."""

    name = "drive_create_files"
    description = (
        "Create and upload multiple UTF-8 text files to La Suite Drive in one "
        "batch. Use this instead of drive_create_file whenever the user requests "
        "two or more new files. Every requested file must include its complete "
        "content. Omit parent_id for My Files, or use a folder UUID returned by "
        "drive_list_items. This does not create binary PDF or DOCX files."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "files": {
                "type": "array",
                "description": "All text files to create in this batch.",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "File name without its final extension.",
                        },
                        "extension": {
                            "type": "string",
                            "description": (
                                "Requested text-file extension, with or without a dot."
                            ),
                        },
                        "content": {
                            "type": "string",
                            "description": "Complete UTF-8 text content for this file.",
                        },
                    },
                    "required": ["file_name", "extension", "content"],
                    "additionalProperties": False,
                },
            },
            "parent_id": {
                "type": "string",
                "description": (
                    "Optional UUID of an existing Drive folder for every file in "
                    "the batch. Omit it to create them in My Files."
                ),
            },
        },
        "required": ["files"],
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
        max_batch_files: int = 50,
    ) -> None:
        self.base_url = base_url
        self.session_id = session_id or ""
        self.csrf_token = csrf_token
        self.upload_acl = upload_acl
        self.max_create_bytes = max_create_bytes
        self.max_batch_files = max_batch_files

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        files = arguments.get("files")
        if not isinstance(files, list) or not files:
            raise DriveAPIError("files must be a non-empty array")
        if len(files) > self.max_batch_files:
            raise DriveAPIError(
                f"A batch can contain at most {self.max_batch_files} files"
            )
        parent_id = arguments.get("parent_id")
        if parent_id is not None and not isinstance(parent_id, str):
            raise DriveAPIError("parent_id must be a string")

        prepared: list[tuple[str, bytes, str]] = []
        for index, file_arguments in enumerate(files, start=1):
            if not isinstance(file_arguments, dict):
                raise DriveAPIError(f"files[{index - 1}] must be an object")
            try:
                prepared.append(
                    _prepare_text_file(
                        file_arguments,
                        max_create_bytes=self.max_create_bytes,
                    )
                )
            except DriveAPIError as exc:
                raise DriveAPIError(f"File {index} is invalid: {exc}") from exc

        upload_acl = resolve_drive_upload_acl(self.base_url, self.upload_acl)
        created: list[dict[str, Any]] = []
        failed: list[dict[str, str]] = []
        for filename, data, content_type in prepared:
            try:
                created.append(
                    create_drive_file(
                        self.base_url,
                        self.session_id,
                        filename=filename,
                        data=data,
                        parent_id=parent_id,
                        csrf_token=self.csrf_token,
                        upload_acl=upload_acl,
                        content_type=content_type,
                    )
                )
            except DriveAPIError as exc:
                failed.append({"filename": filename, "error": str(exc)})

        status = "created" if not failed else "partially_created" if created else "failed"
        return {
            "status": status,
            "requested_count": len(files),
            "created_count": len(created),
            "failed_count": len(failed),
            "complete": not failed,
            "files": created,
            "failures": failed,
            "artifacts": [
                result["artifact"] for result in created if "artifact" in result
            ],
        }
