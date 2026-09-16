"""Read a bounded text-based file from the configured local workspace."""

from pathlib import Path
from typing import Any

from pydantic import ValidationError

from agent.artifacts import Artifact
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError
from services.local_files import read_local_text


class LocalFilesReadTextAgent(SpecialistAgent):
    name = "local_files_read_text"
    description = (
        "Read the content of a local text-based file such as CSV, TSV, TXT, "
        "Markdown, JSON, XML, YAML, or LOG. Use this after local_files_list_items "
        "when the user wants to inspect an unknown local file, understand its "
        "contents, or choose a descriptive name before renaming it. Accept a local "
        "file artifact when available. UTF-8 with or without BOM, UTF-16 with BOM, "
        "and Windows-1252 text are supported."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "relative_path": {
                "type": "string",
                "description": "File path relative to LOCAL_FILES_ROOT.",
            },
            "artifact": {
                **Artifact.model_json_schema(),
                "description": "Optional local file artifact returned by another capability.",
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
        root: Path,
        *,
        max_read_bytes: int = 20 * 1024 * 1024,
        max_text_characters: int = 100_000,
    ) -> None:
        self.root = root
        self.max_read_bytes = max_read_bytes
        self.max_text_characters = max_text_characters

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        if arguments.get("artifact") is not None:
            try:
                artifact = Artifact.model_validate(arguments["artifact"])
            except ValidationError as exc:
                raise LocalFilesError("artifact is invalid") from exc
            if artifact.kind != "file" or artifact.location != "local":
                raise LocalFilesError("Text reading requires a local file artifact")
            relative_path = artifact.reference
        else:
            relative_path = arguments.get("relative_path")
            if not isinstance(relative_path, str):
                raise LocalFilesError("relative_path must be a string")
        return read_local_text(
            self.root,
            relative_path,
            max_bytes=self.max_read_bytes,
            max_characters=self.max_text_characters,
        )
