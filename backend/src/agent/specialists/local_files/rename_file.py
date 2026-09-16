"""Rename a file inside the configured local workspace."""

from pathlib import Path
from typing import Any

from pydantic import ValidationError

from agent.artifacts import Artifact
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError
from services.local_files import rename_local_file


class LocalFilesRenameFileAgent(SpecialistAgent):
    name = "local_files_rename_file"
    description = (
        "Rename one existing local file without moving it to another directory. "
        "Use only when the user explicitly asks for a rename. Accept a local file "
        "artifact from local_files_list_items when available. If new_name has no "
        "extension, preserve the existing extension. Never overwrite another file."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "relative_path": {
                "type": "string",
                "description": "Current path relative to LOCAL_FILES_ROOT.",
            },
            "artifact": {
                **Artifact.model_json_schema(),
                "description": "Optional local file artifact returned by another capability.",
            },
            "new_name": {
                "type": "string",
                "description": (
                    "New filename in the same directory. The current extension is "
                    "preserved when this value has no extension."
                ),
            },
        },
        "required": ["new_name"],
        "anyOf": [
            {"required": ["relative_path"]},
            {"required": ["artifact"]},
        ],
        "additionalProperties": False,
    }

    def __init__(self, root: Path) -> None:
        self.root = root

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        new_name = arguments.get("new_name")
        if not isinstance(new_name, str):
            raise LocalFilesError("new_name must be a string")
        if arguments.get("artifact") is not None:
            try:
                artifact = Artifact.model_validate(arguments["artifact"])
            except ValidationError as exc:
                raise LocalFilesError("artifact is invalid") from exc
            if artifact.kind != "file" or artifact.location != "local":
                raise LocalFilesError("Rename requires a local file artifact")
            relative_path = artifact.reference
        else:
            relative_path = arguments.get("relative_path")
            if not isinstance(relative_path, str):
                raise LocalFilesError("relative_path must be a string")
        return rename_local_file(
            self.root,
            relative_path=relative_path,
            new_name=new_name,
        )
