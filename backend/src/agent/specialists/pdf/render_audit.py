"""Render a complete in-memory audit artifact as a local PDF."""

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
from agent.errors import PdfError
from services.pdf import create_local_pdf


class PdfRenderAuditAgent(SpecialistAgent):
    name = "pdf_render_audit"
    description = (
        "Render a complete audit_report artifact as a local PDF without sending the "
        "full report back through the language model. Preserve every criterion, source "
        "entry, citation, finding, limitation, and corrective action. Use this whenever "
        "an audit capability returned an audit_report artifact and the user requested "
        "a PDF report."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "artifact": {
                **Artifact.model_json_schema(),
                "description": "The audit_report artifact returned by an audit capability.",
            },
            "directory": {
                "type": "string",
                "description": "Existing destination directory relative to LOCAL_FILES_ROOT.",
            },
            "file_name": {
                "type": "string",
                "description": "Output filename without the .pdf extension.",
            },
            "title": {
                "type": "string",
                "description": "Optional title; defaults to file_name.",
            },
        },
        "required": ["artifact", "directory", "file_name"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        root: Path,
        *,
        max_body_characters: int = 200_000,
        artifact_store: MemoryArtifactStore = memory_artifact_store,
    ) -> None:
        self.root = root
        self.max_body_characters = max_body_characters
        self.artifact_store = artifact_store

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        try:
            artifact = Artifact.model_validate(arguments.get("artifact"))
        except ValidationError as exc:
            raise PdfError("artifact must be a valid audit-report artifact") from exc
        for key in ("directory", "file_name"):
            if not isinstance(arguments.get(key), str):
                raise PdfError(f"{key} must be a string")
        title = arguments.get("title", arguments["file_name"])
        if not isinstance(title, str):
            raise PdfError("title must be a string")
        try:
            payload = self.artifact_store.get(artifact, expected_kind="audit_report")
        except ArtifactNotFoundError as exc:
            raise PdfError(str(exc.args[0])) from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("audit"), str):
            raise PdfError("The audit artifact contains invalid data")
        clean_name = arguments["file_name"].strip()
        if clean_name.lower().endswith(".pdf"):
            clean_name = clean_name[:-4]
        created = create_local_pdf(
            self.root,
            directory=arguments["directory"],
            file_name=clean_name,
            title=title.strip() or clean_name or "Audit report",
            body_text=payload["audit"],
            max_body_characters=self.max_body_characters,
        )
        return {
            "status": "created",
            "source_audit": artifact.tool_value(),
            **created,
        }
