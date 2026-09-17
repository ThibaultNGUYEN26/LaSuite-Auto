"""Create folders in La Suite Drive."""

from __future__ import annotations

from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import create_drive_folder


class DriveCreateFolderAgent(SpecialistAgent):
    name = "drive_create_folder"
    description = (
        "Create a folder in La Suite Drive. Omit parent_id to create it at the "
        "top of My Files, or use the UUID of an existing Drive folder to create "
        "a nested folder. Return a reusable folder artifact so subsequent files "
        "or folders can be created inside it."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "minLength": 1,
                "maxLength": 255,
                "description": "Name of the new Drive folder.",
            },
            "parent_id": {
                "type": "string",
                "format": "uuid",
                "description": (
                    "Optional UUID of an existing Drive folder. Omit it for "
                    "the top of My Files."
                ),
            },
        },
        "required": ["title"],
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
        title = arguments.get("title")
        parent_id = arguments.get("parent_id")
        if not isinstance(title, str):
            raise DriveAPIError("title must be a string")
        if parent_id is not None and not isinstance(parent_id, str):
            raise DriveAPIError("parent_id must be a string")
        return create_drive_folder(
            self.base_url,
            self.session_id,
            title=title,
            parent_id=parent_id,
            csrf_token=self.csrf_token,
        )


__all__ = ["DriveCreateFolderAgent"]
