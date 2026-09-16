"""Upload an existing local file to La Suite Drive."""

from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from agent.artifacts import Artifact
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import create_drive_file, resolve_drive_upload_acl
from services.local_files import read_local_file, resolve_local_file


def _validate_destination_name(value: str) -> str:
    name = value.strip()
    if (
        not name
        or name in {".", ".."}
        or Path(name).name != name
        or any(character in name for character in '<>:"/\\|?*')
        or name.endswith((" ", "."))
    ):
        raise DriveAPIError("destination_name contains invalid characters")
    return name


class DriveUploadFileAgent(SpecialistAgent):
    name = "drive_upload_file"
    description = (
        "Upload an existing local file to La Suite Drive without changing its bytes. "
        "Use this for PDFs, images, archives, office documents, executables, and other "
        "binary or text files, but only when the user explicitly asks to upload one. "
        "The source path must be relative to LOCAL_FILES_ROOT. Omit parent_id for My "
        "Files, or use a folder UUID returned by drive_list_items."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "relative_path": {
                "type": "string",
                "description": (
                    "Existing file path relative to LOCAL_FILES_ROOT, for example "
                    "Downloads/report.pdf."
                ),
            },
            "artifact": {
                **Artifact.model_json_schema(),
                "description": (
                    "Optional typed local file artifact returned by another block. "
                    "Use this instead of relative_path when available."
                ),
            },
            "parent_id": {
                "type": "string",
                "description": (
                    "Optional destination Drive folder UUID. Omit it for My Files."
                ),
            },
            "destination_name": {
                "type": "string",
                "description": (
                    "Optional full filename to use in Drive, including its extension. "
                    "Omit it to preserve the local filename."
                ),
            },
        },
        "anyOf": [
            {"required": ["relative_path"]},
            {"required": ["artifact"]},
        ],
        "additionalProperties": False,
    }

    def __init__(
        self,
        base_url: str,
        session_id: str | None,
        local_files_root: Path,
        *,
        csrf_token: str | None = None,
        upload_acl: str | None = None,
        max_upload_bytes: int = 50 * 1024 * 1024,
    ) -> None:
        self.base_url = base_url
        self.session_id = session_id or ""
        self.local_files_root = local_files_root
        self.csrf_token = csrf_token
        self.upload_acl = upload_acl
        self.max_upload_bytes = max_upload_bytes

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        artifact_value = arguments.get("artifact")
        if artifact_value is not None:
            try:
                artifact = Artifact.model_validate(artifact_value)
            except ValidationError as exc:
                raise DriveAPIError("artifact is invalid") from exc
            if artifact.kind != "file" or artifact.location != "local":
                raise DriveAPIError("Drive upload requires a local file artifact")
            relative_path = artifact.reference
        else:
            relative_path = arguments.get("relative_path")
            if not isinstance(relative_path, str):
                raise DriveAPIError("Provide relative_path or a local file artifact")
        parent_id = arguments.get("parent_id")
        if parent_id is not None and not isinstance(parent_id, str):
            raise DriveAPIError("parent_id must be a string")
        destination_name = arguments.get("destination_name")
        if destination_name is not None and not isinstance(destination_name, str):
            raise DriveAPIError("destination_name must be a string")

        source_path = resolve_local_file(self.local_files_root, relative_path)
        filename = (
            _validate_destination_name(destination_name)
            if destination_name is not None
            else source_path.name
        )
        data = read_local_file(
            self.local_files_root,
            relative_path,
            max_bytes=self.max_upload_bytes,
        )
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        result = create_drive_file(
            self.base_url,
            self.session_id,
            filename=filename,
            data=data,
            parent_id=parent_id,
            csrf_token=self.csrf_token,
            upload_acl=resolve_drive_upload_acl(self.base_url, self.upload_acl),
            content_type=content_type,
        )
        result.update(
            {
                "source_relative_path": source_path.relative_to(
                    self.local_files_root.expanduser().resolve()
                ).as_posix(),
                "content_type": content_type,
            }
        )
        return result
