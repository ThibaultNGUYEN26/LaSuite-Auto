"""Read a bounded text-based file from La Suite Drive."""

from typing import Any

from pydantic import ValidationError

from agent.artifacts import Artifact
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import read_drive_text


class DriveReadTextAgent(SpecialistAgent):
    name = "drive_read_text"
    description = (
        "Read the content of a Drive CSV, TSV, TXT, Markdown, JSON, XML, YAML, "
        "or LOG file. Use this after drive_list_items when the user wants to "
        "inspect an unknown Drive file, understand its contents, or choose a "
        "descriptive name before renaming it. Prefer the Drive file artifact "
        "returned by drive_list_items."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "item_id": {"type": "string", "description": "Drive file UUID."},
            "filename": {
                "type": "string",
                "description": "Drive filename including its extension.",
            },
            "artifact": {
                **Artifact.model_json_schema(),
                "description": "Optional Drive file artifact returned by another capability.",
            },
        },
        "anyOf": [
            {"required": ["item_id", "filename"]},
            {"required": ["artifact"]},
        ],
        "additionalProperties": False,
    }

    def __init__(
        self,
        base_url: str,
        session_id: str | None,
        *,
        max_download_bytes: int = 20 * 1024 * 1024,
        max_text_characters: int = 100_000,
    ) -> None:
        self.base_url = base_url
        self.session_id = session_id or ""
        self.max_download_bytes = max_download_bytes
        self.max_text_characters = max_text_characters

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        if arguments.get("artifact") is not None:
            try:
                artifact = Artifact.model_validate(arguments["artifact"])
            except ValidationError as exc:
                raise DriveAPIError("artifact is invalid") from exc
            if artifact.kind != "file" or artifact.location != "drive":
                raise DriveAPIError("Text reading requires a Drive file artifact")
            if not artifact.name:
                raise DriveAPIError("The Drive artifact has no filename")
            item_id, filename = artifact.reference, artifact.name
        else:
            item_id = arguments.get("item_id")
            filename = arguments.get("filename")
            if not isinstance(item_id, str):
                raise DriveAPIError("item_id must be a string")
            if not isinstance(filename, str):
                raise DriveAPIError("filename must be a string")
        return read_drive_text(
            self.base_url,
            self.session_id,
            item_id,
            filename=filename,
            max_bytes=self.max_download_bytes,
            max_characters=self.max_text_characters,
        )
