"""Rename a file in La Suite Drive."""

from typing import Any

from pydantic import ValidationError

from agent.artifacts import Artifact
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import rename_drive_file


class DriveRenameFileAgent(SpecialistAgent):
    name = "drive_rename_file"
    description = (
        "Rename one existing Drive file without changing or re-uploading its "
        "contents. Use only when the user explicitly asks for a rename. Accept a "
        "Drive file artifact from drive_list_items when available. The current "
        "file extension is preserved and cannot be changed by renaming."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "item_id": {"type": "string", "description": "Drive file UUID."},
            "artifact": {
                **Artifact.model_json_schema(),
                "description": "Optional Drive file artifact returned by another capability.",
            },
            "new_name": {
                "type": "string",
                "description": (
                    "New display name, with or without the existing extension. "
                    "Do not supply a different extension."
                ),
            },
        },
        "required": ["new_name"],
        "anyOf": [
            {"required": ["item_id"]},
            {"required": ["artifact"]},
        ],
        "additionalProperties": False,
    }

    def __init__(
        self,
        base_url: str,
        session_id: str | None,
        *,
        csrf_token: str | None = None,
    ) -> None:
        self.base_url = base_url
        self.session_id = session_id or ""
        self.csrf_token = csrf_token

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        new_name = arguments.get("new_name")
        if not isinstance(new_name, str):
            raise DriveAPIError("new_name must be a string")
        if arguments.get("artifact") is not None:
            try:
                artifact = Artifact.model_validate(arguments["artifact"])
            except ValidationError as exc:
                raise DriveAPIError("artifact is invalid") from exc
            if artifact.kind != "file" or artifact.location != "drive":
                raise DriveAPIError("Rename requires a Drive file artifact")
            item_id = artifact.reference
        else:
            item_id = arguments.get("item_id")
            if not isinstance(item_id, str):
                raise DriveAPIError("item_id must be a string")
        return rename_drive_file(
            self.base_url,
            self.session_id,
            item_id,
            new_name=new_name,
            csrf_token=self.csrf_token,
        )
