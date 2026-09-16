"""List files below the configured local workspace."""

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError
from services.local_files import list_local_items


class LocalFilesListItemsAgent(SpecialistAgent):
    name = "local_files_list_items"
    description = (
        "List files and folders on this computer under the configured local-files "
        "workspace (normally the user's home folder), including subfolders by "
        "default. The directory parameter can select Downloads, Documents, Desktop, "
        "or a folder path returned by folder creation. Use this to search or inspect "
        "the contents of a specific local folder. Use this for requests about local "
        "files or the computer. Do not use it for La Suite Drive."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": (
                    "Optional directory relative to the configured local-files root, "
                    "for example Downloads or Documents/Reports. Defaults to the root."
                ),
            },
            "limit": {"type": "integer", "minimum": 1, "maximum": 500},
            "recursive": {"type": "boolean", "description": "Defaults to true."},
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "description": "Maximum traversal depth. The hard limit is 5.",
            },
        },
        "additionalProperties": False,
    }

    def __init__(self, root: Path) -> None:
        self.root = root

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        directory = arguments.get("directory", ".")
        limit = arguments.get("limit", 100)
        recursive = arguments.get("recursive", True)
        max_depth = arguments.get("max_depth", 5)
        if not isinstance(directory, str):
            raise LocalFilesError("directory must be a string")
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise LocalFilesError("limit must be an integer")
        if not isinstance(recursive, bool):
            raise LocalFilesError("recursive must be a boolean")
        if not isinstance(max_depth, int) or isinstance(max_depth, bool):
            raise LocalFilesError("max_depth must be an integer")
        return list_local_items(
            self.root,
            directory=directory,
            limit=limit,
            recursive=recursive,
            max_depth=max_depth,
        )
