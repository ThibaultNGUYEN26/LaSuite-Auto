"""Analyze CSV, ODS, or Grist data into a portable analysis artifact."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import ValidationError

from agent.artifact_store import MemoryArtifactStore, memory_artifact_store
from agent.artifacts import Artifact
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DataAnalysisError, DriveAPIError, GristAPIError, LocalFilesError
from services.drive import download_drive_file
from services.grist import read_grist_table
from services.local_files import read_local_file
from services.tabular_analysis import (
    analyze_table,
    parse_csv_data,
    parse_ods_data,
)


CSV_MEDIA_TYPES = {"text/csv", "application/csv", "application/vnd.ms-excel"}
ODS_MEDIA_TYPE = "application/vnd.oasis.opendocument.spreadsheet"


class AnalyzeTableAgent(SpecialistAgent):
    name = "data_analyze_table"
    description = (
        "Perform a comprehensive statistical analysis of a CSV file, OpenDocument "
        "ODS spreadsheet, or Grist document. Produce a typed in-memory analysis "
        "artifact containing data-quality checks, distributions, outliers, date-based "
        "trends, charts, period changes, category concentration, correlations, "
        "methodology, and limitations. Use the user's exact analytical question as "
        "question. When a report is requested, pass the returned artifact to "
        "pdf_render_analysis; do not claim a report exists after analysis alone."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "artifact": {
                **Artifact.model_json_schema(),
                "description": (
                    "A CSV/ODS file artifact or Grist document artifact returned "
                    "by another block. Prefer this over source_type and source."
                ),
            },
            "source_type": {
                "type": "string",
                "enum": ["local", "drive", "grist"],
                "description": "Source to use when no artifact is available.",
            },
            "source": {
                "type": "string",
                "description": (
                    "Local relative path, Drive item UUID, or Grist document ID."
                ),
            },
            "source_name": {
                "type": "string",
                "description": (
                    "Filename including .csv or .ods when source is a Drive UUID."
                ),
            },
            "table_id": {
                "type": "string",
                "description": "Optional Grist table ID; the first data table is used otherwise.",
            },
            "question": {
                "type": "string",
                "description": "The user's analytical question, or a request for general analysis.",
            },
            "date_column": {
                "type": "string",
                "description": "Optional column that represents time for trend analysis.",
            },
            "value_columns": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional numeric columns to prioritize.",
            },
        },
        "required": ["question"],
        "anyOf": [
            {"required": ["artifact"]},
            {"required": ["source_type", "source"]},
        ],
        "additionalProperties": False,
    }

    def __init__(
        self,
        *,
        local_files_root: Path,
        drive_base_url: str,
        drive_session_id: str | None,
        grist_base_url: str,
        grist_api_key: str | None,
        max_source_bytes: int = 20 * 1024 * 1024,
        max_rows: int = 10_000,
        artifact_store: MemoryArtifactStore = memory_artifact_store,
    ) -> None:
        self.local_files_root = local_files_root
        self.drive_base_url = drive_base_url
        self.drive_session_id = drive_session_id or ""
        self.grist_base_url = grist_base_url
        self.grist_api_key = grist_api_key or ""
        self.max_source_bytes = max_source_bytes
        self.max_rows = max_rows
        self.artifact_store = artifact_store

    def _artifact_source(self, value: Any) -> tuple[str, str, str | None]:
        try:
            artifact = Artifact.model_validate(value)
        except ValidationError as exc:
            raise DataAnalysisError("artifact is invalid") from exc
        if artifact.kind == "grist_document":
            return "grist", artifact.reference, artifact.name
        if artifact.kind != "file":
            raise DataAnalysisError("Analysis requires a file or Grist document artifact")
        if artifact.location not in {"local", "drive"}:
            raise DataAnalysisError("The file artifact must come from local files or Drive")
        return artifact.location, artifact.reference, artifact.name

    def _load_file(self, source_type: str, source: str) -> bytes:
        try:
            if source_type == "local":
                return read_local_file(
                    self.local_files_root,
                    source,
                    max_bytes=self.max_source_bytes,
                )
            return download_drive_file(
                self.drive_base_url,
                self.drive_session_id,
                source,
                max_bytes=self.max_source_bytes,
            )
        except (LocalFilesError, DriveAPIError) as exc:
            raise DataAnalysisError(str(exc)) from exc

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        question = arguments.get("question")
        if not isinstance(question, str):
            raise DataAnalysisError("question must be a string")
        table_id = arguments.get("table_id")
        if table_id is not None and not isinstance(table_id, str):
            raise DataAnalysisError("table_id must be a string")
        date_column = arguments.get("date_column")
        if date_column is not None and not isinstance(date_column, str):
            raise DataAnalysisError("date_column must be a string")
        value_columns = arguments.get("value_columns")
        if value_columns is not None and (
            not isinstance(value_columns, list)
            or not all(isinstance(value, str) for value in value_columns)
        ):
            raise DataAnalysisError("value_columns must be an array of strings")

        if arguments.get("artifact") is not None:
            source_type, source, artifact_name = self._artifact_source(arguments["artifact"])
        else:
            source_type = arguments.get("source_type")
            source = arguments.get("source")
            artifact_name = None
            if source_type not in {"local", "drive", "grist"}:
                raise DataAnalysisError("source_type must be local, drive, or grist")
            if not isinstance(source, str) or not source.strip():
                raise DataAnalysisError("source must be a non-empty string")

        source_name = arguments.get("source_name") or artifact_name or source
        if not isinstance(source_name, str):
            raise DataAnalysisError("source_name must be a string")
        if source_type == "grist":
            try:
                headers, rows, selected_table, truncated = read_grist_table(
                    self.grist_base_url,
                    self.grist_api_key,
                    document_id=source,
                    table_id=table_id,
                    max_rows=self.max_rows,
                )
            except GristAPIError as exc:
                raise DataAnalysisError(str(exc)) from exc
            source_name = f"{source_name} / {selected_table}"
        else:
            data = self._load_file(source_type, source)
            lower_name = source_name.lower()
            if lower_name.endswith(".ods"):
                headers, rows, truncated = parse_ods_data(data, max_rows=self.max_rows)
            elif lower_name.endswith(".csv"):
                headers, rows, truncated = parse_csv_data(data, max_rows=self.max_rows)
            else:
                raise DataAnalysisError(
                    "The selected file must have a .csv or .ods filename"
                )

        analysis = analyze_table(
            headers,
            rows,
            question=question,
            requested_date_column=date_column,
            requested_value_columns=value_columns,
            truncated=truncated,
        )
        artifact = self.artifact_store.put(
            {"analysis": analysis, "source_name": source_name},
            kind="data_analysis",
            media_type="application/vnd.lasuite.data-analysis+json",
            name=f"Analysis of {source_name}",
            metadata={
                "source": source_name,
                "question": question,
                "rows": analysis["row_count"],
                "columns": analysis["column_count"],
                "truncated": analysis["truncated"],
            },
        )

        return {
            "status": "analyzed",
            "source": source_name,
            "rows_analyzed": analysis["row_count"],
            "columns_analyzed": analysis["column_count"],
            "truncated": analysis["truncated"],
            "date_column": analysis["date_column"],
            "numeric_statistics": analysis["numeric_statistics"],
            "trends": [
                {key: value for key, value in trend.items() if key != "series"}
                for trend in analysis["trends"]
            ],
            "correlations": analysis["correlations"],
            "findings": analysis["findings"],
            "limitations": analysis["limitations"],
            "artifact": artifact.tool_value(),
            "next_action": (
                "Use pdf_render_analysis with this artifact when the user requested "
                "a report. The analysis itself has not created a file."
            ),
        }
