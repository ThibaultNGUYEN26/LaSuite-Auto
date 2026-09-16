"""Render a structured data-analysis artifact as a comprehensive PDF report."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import ValidationError

from agent.artifact_store import (
    ArtifactNotFoundError,
    MemoryArtifactStore,
    memory_artifact_store,
)
from agent.artifacts import Artifact
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError, PdfError
from services.local_files import create_local_binary_file
from services.pdf_report import render_pdf_report


class PdfRenderAnalysisAgent(SpecialistAgent):
    name = "pdf_render_analysis"
    description = (
        "Render a data_analysis artifact as a comprehensive PDF report with an "
        "executive summary, quality assessment, statistics, trend charts, "
        "relationships, methodology, and limitations. Use this after "
        "data_analyze_table whenever the user asks for an analysis report."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "artifact": {
                **Artifact.model_json_schema(),
                "description": "The data_analysis artifact returned by data_analyze_table.",
            },
            "directory": {
                "type": "string",
                "description": (
                    "Existing destination directory relative to the local workspace. "
                    "Use . unless the user selected another local folder."
                ),
                "default": ".",
            },
            "file_name": {
                "type": "string",
                "description": "Output filename without the .pdf extension.",
            },
            "title": {
                "type": "string",
                "description": "Optional report title; defaults to file_name.",
            },
        },
        "required": ["artifact", "directory", "file_name"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        root: Path,
        *,
        max_report_bytes: int = 5 * 1024 * 1024,
        artifact_store: MemoryArtifactStore = memory_artifact_store,
    ) -> None:
        self.root = root
        self.max_report_bytes = max_report_bytes
        self.artifact_store = artifact_store

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        try:
            artifact = Artifact.model_validate(arguments.get("artifact"))
        except ValidationError as exc:
            raise PdfError("artifact must be a valid data-analysis artifact") from exc
        for key in ("directory", "file_name"):
            if not isinstance(arguments.get(key), str):
                raise PdfError(f"{key} must be a string")
        title = arguments.get("title", arguments["file_name"])
        if not isinstance(title, str):
            raise PdfError("title must be a string")
        clean_name = arguments["file_name"].strip()
        if clean_name.lower().endswith(".pdf"):
            clean_name = clean_name[:-4]
        try:
            payload = self.artifact_store.get(
                artifact, expected_kind="data_analysis"
            )
        except ArtifactNotFoundError as exc:
            raise PdfError(str(exc.args[0])) from exc
        if not isinstance(payload, dict) or not isinstance(
            payload.get("analysis"), dict
        ):
            raise PdfError("The analysis artifact contains invalid data")
        report_data = render_pdf_report(
            payload["analysis"],
            title=title.strip() or clean_name or "Data analysis report",
            source_name=str(payload.get("source_name") or "Unknown source"),
        )
        try:
            created = create_local_binary_file(
                self.root,
                directory=arguments["directory"],
                file_name=clean_name,
                extension="pdf",
                data=report_data,
                max_bytes=self.max_report_bytes,
                media_type="application/pdf",
            )
        except LocalFilesError as exc:
            raise PdfError(str(exc)) from exc
        return {
            "status": "created",
            "source_analysis": artifact.tool_value(),
            "report": created,
            "artifact": created["artifact"],
        }
