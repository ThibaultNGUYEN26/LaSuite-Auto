"""Create a folder in the configured local workspace."""

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError
from services.local_files import create_local_directory


class LocalFilesCreateFolderAgent(SpecialistAgent):
    name = "local_files_create_folder"
    description = (
        "Create a new folder under an existing folder in the local workspace. Use "
        "this when the user asks to organize files into a folder such as Client 1. "
        "Return the new relative path so another capability can immediately create, "
        "move, or search files inside it. Never overwrite an existing path."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "parent_directory": {
                "type": "string",
                "description": (
                    "Existing parent relative to LOCAL_FILES_ROOT, such as Downloads. "
                    "Use . for the workspace root."
                ),
            },
            "folder_name": {
                "type": "string",
                "description": "Name of the new direct child folder, such as Client 1.",
            },
        },
        "required": ["parent_directory", "folder_name"],
        "additionalProperties": False,
    }

    def __init__(self, root: Path) -> None:
        self.root = root

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        parent_directory = arguments.get("parent_directory")
        folder_name = arguments.get("folder_name")
        if not isinstance(parent_directory, str):
            raise LocalFilesError("parent_directory must be a string")
        if not isinstance(folder_name, str):
            raise LocalFilesError("folder_name must be a string")
        return create_local_directory(
            self.root,
            parent_directory=parent_directory,
            folder_name=folder_name,
        )
