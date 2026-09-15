"""Drive tree-listing specialist."""

from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import list_drive_items


class DriveListItemsAgent(SpecialistAgent):
    name = "drive_list_items"
    description = (
        "List the authenticated user's files and folders in La Suite Drive, including "
        "nested folder contents by default. Use this to discover item UUIDs before "
        "reading a Drive PDF. This reads Drive, not the computer's local filesystem."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "limit": {"type": "integer", "minimum": 1, "maximum": 500},
            "recursive": {"type": "boolean", "description": "Defaults to true."},
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "description": "Maximum traversal depth. The hard limit is 5.",
            },
            "folder_id": {"type": "string", "format": "uuid"},
        },
        "additionalProperties": False,
    }

    def __init__(self, base_url: str, session_id: str | None) -> None:
        self.base_url = base_url
        self.session_id = session_id

    def execute(self, arguments: dict[str, Any], context: DelegationContext) -> dict[str, Any]:
        del context
        limit = arguments.get("limit", 100)
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise DriveAPIError("limit must be an integer")
        recursive = arguments.get("recursive", True)
        if not isinstance(recursive, bool):
            raise DriveAPIError("recursive must be a boolean")
        max_depth = arguments.get("max_depth", 5)
        if not isinstance(max_depth, int) or isinstance(max_depth, bool):
            raise DriveAPIError("max_depth must be an integer")
        folder_id = arguments.get("folder_id")
        if folder_id is not None and not isinstance(folder_id, str):
            raise DriveAPIError("folder_id must be a string")
        return list_drive_items(
            self.base_url, self.session_id or "", limit=limit, recursive=recursive,
            max_depth=max_depth, folder_id=folder_id,
        )
