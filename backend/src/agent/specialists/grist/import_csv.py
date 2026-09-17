"""Import CSV data from text, a local file, or La Suite Drive into Grist."""

from __future__ import annotations

import csv
import io
import re
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from agent.artifacts import Artifact
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import GristAPIError, LocalFilesError
from services.drive import download_drive_file
from services.grist import import_csv_document
from services.local_files import read_local_file, resolve_local_file


class GristImportCsvAgent(SpecialistAgent):
    name = "grist_import_csv"
    description = (
        "Import CSV data as a new saved Grist document. Use only when the user "
        "explicitly asks to send or import CSV data into Grist. The source can be "
        "CSV text from the conversation, a relative local CSV path, or a Drive item "
        "UUID. Use grist_list_workspaces first when a destination workspace ID is "
        "needed. This creates a new Grist document and never replaces an existing one."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "source_type": {
                "type": "string",
                "enum": ["content", "local", "drive"],
                "description": "Where the CSV data comes from.",
            },
            "source": {
                "type": "string",
                "description": (
                    "CSV text, a path relative to LOCAL_FILES_ROOT, or a Drive item "
                    "UUID, according to source_type."
                ),
            },
            "artifact": {
                **Artifact.model_json_schema(),
                "description": (
                    "Optional CSV file artifact returned by another block. Use this "
                    "instead of source_type and source when available."
                ),
            },
            "document_name": {
                "type": "string",
                "description": "Name for the new Grist document.",
            },
            "workspace_id": {
                "type": "integer",
                "description": (
                    "Destination Grist workspace ID. Omit only when a default "
                    "GRIST_WORKSPACE_ID is configured."
                ),
            },
        },
        "required": ["document_name"],
        "anyOf": [
            {"required": ["source_type", "source"]},
            {"required": ["artifact"]},
        ],
        "additionalProperties": False,
    }

    def __init__(
        self,
        base_url: str,
        api_key: str | None,
        *,
        org_id: str,
        workspace_id: int | None,
        local_files_root: Path,
        drive_base_url: str,
        drive_session_id: str | None,
        max_import_bytes: int = 10 * 1024 * 1024,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key or ""
        self.org_id = org_id
        self.workspace_id = workspace_id
        self.local_files_root = local_files_root
        self.drive_base_url = drive_base_url
        self.drive_session_id = drive_session_id or ""
        self.max_import_bytes = max_import_bytes

    def _load_source(self, source_type: str, source: str) -> bytes:
        if source_type == "content":
            return source.encode("utf-8")
        if source_type == "local":
            try:
                path = resolve_local_file(self.local_files_root, source)
                if path.suffix.lower() != ".csv":
                    raise GristAPIError("The selected local file is not a CSV file")
                return read_local_file(
                    self.local_files_root,
                    source,
                    max_bytes=self.max_import_bytes,
                )
            except LocalFilesError as exc:
                raise GristAPIError(str(exc)) from exc
        if source_type == "drive":
            return download_drive_file(
                self.drive_base_url,
                self.drive_session_id,
                source,
                max_bytes=self.max_import_bytes,
            )
        raise GristAPIError("source_type must be content, local, or drive")

    def _load_artifact(self, value: Any) -> tuple[bytes, str]:
        try:
            artifact = Artifact.model_validate(value)
        except ValidationError as exc:
            raise GristAPIError("artifact is invalid") from exc
        if artifact.kind != "file":
            raise GristAPIError("Grist import requires a file artifact")
        if artifact.media_type not in {
            "text/csv",
            "application/csv",
            "application/vnd.ms-excel",
        } and not (artifact.name or "").lower().endswith(".csv"):
            raise GristAPIError("The selected artifact is not CSV data")
        if artifact.location == "local":
            return self._load_source("local", artifact.reference), "local"
        if artifact.location == "drive":
            return self._load_source("drive", artifact.reference), "drive"
        raise GristAPIError("CSV artifacts must come from local files or Drive")

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        if not isinstance(arguments.get("document_name"), str):
            raise GristAPIError("document_name must be a string")
        workspace_id = arguments.get("workspace_id", self.workspace_id)
        if not isinstance(workspace_id, int) or isinstance(workspace_id, bool):
            raise GristAPIError(
                "Choose a Grist workspace before importing this CSV."
            )

        if arguments.get("artifact") is not None:
            data, source_type = self._load_artifact(arguments["artifact"])
        else:
            for key in ("source_type", "source"):
                if not isinstance(arguments.get(key), str):
                    raise GristAPIError(f"{key} must be a string")
            source_type = arguments["source_type"]
            data = self._load_source(source_type, arguments["source"])
        if len(data) > self.max_import_bytes:
            raise GristAPIError(
                f"CSV exceeds the configured {self.max_import_bytes}-byte import limit"
            )
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise GristAPIError("CSV must use UTF-8 text encoding") from exc
        if not text.strip() or "\x00" in text:
            raise GristAPIError("CSV content is empty or invalid")
        try:
            rows = list(csv.reader(io.StringIO(text)))
        except csv.Error as exc:
            raise GristAPIError(f"CSV content could not be parsed: {exc}") from exc
        if not rows or not any(cell.strip() for cell in rows[0]):
            raise GristAPIError("CSV must contain a header row")

        document_name = arguments["document_name"].strip()
        if not document_name or len(document_name) > 255:
            raise GristAPIError("document_name must contain 1 to 255 characters")
        safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", document_name).strip("._")
        filename = f"{safe_stem or 'import'}.csv"
        result = import_csv_document(
            self.base_url,
            self.api_key,
            workspace_id=workspace_id,
            document_name=document_name,
            filename=filename,
            csv_data=data,
            org_id=self.org_id,
            markdown_columns=tuple(
                header.strip()
                for header in rows[0]
                if header.strip().casefold() in {"reference sources", "client sources"}
            ),
        )
        result.update(
            {
                "source_type": source_type,
                "data_rows": max(0, len(rows) - 1),
                "columns": len(rows[0]),
            }
        )
        return result
