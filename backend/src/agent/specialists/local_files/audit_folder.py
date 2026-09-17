"""Audit a complete local client folder against one reference PDF."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

from agent.artifact_store import MemoryArtifactStore, memory_artifact_store
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import AlbertAPIError, LocalFilesError
from agent.specialists.local_files.summarize_pdf import LocalFilesSummarizePdfAgent
from agent.specialists.local_files.summarize_pdfs import LocalFilesSummarizePdfsAgent
from providers.albert import AlbertClient
from services.pdf_audit import audit_folder_against_reference
from services.pdf_memory import find_pdf_memory
from services.local_files import create_local_text_file


class LocalFilesAuditFolderAgent(SpecialistAgent):
    name = "local_files_audit_folder"
    description = (
        "Audit one client folder or multi-document client corpus against one local "
        "audit/reference PDF. Use this when the subject is a folder, a client with "
        "several documents, or the user says to audit a client identified earlier. "
        "It discovers and assesses every supported PDF, CSV, and text evidence file "
        "in the selected folder in one operation; never replace the corpus with its "
        "first file. It automatically creates or refreshes reusable memories for the "
        "reference and every client PDF, while grounding audit verdicts in original "
        "pages and CSV/text lines. Its report includes a reusable source register "
        "with stable IDs, exact local paths, and file artifacts so evidence can be "
        "reopened in later questions. When csv_relative_path is provided, it also "
        "exports the complete criterion matrix as a UTF-8 CSV artifact suitable for "
        "direct Grist import. Proceed without asking to continue when the "
        "reference and client folder are already known."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "audit_relative_path": {
                "type": "string",
                "description": "Audit/reference PDF path relative to LOCAL_FILES_ROOT.",
            },
            "client_directory": {
                "type": "string",
                "description": "Client evidence folder relative to LOCAL_FILES_ROOT.",
            },
            "focus": {
                "type": "string",
                "description": "Optional audit scope. Omit for every criterion.",
            },
            "recursive": {
                "type": "boolean",
                "description": "Include evidence in subfolders. Defaults to true.",
                "default": True,
            },
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "default": 5,
                "description": "How deeply to inspect the selected client folder.",
            },
            "csv_relative_path": {
                "type": "string",
                "description": (
                    "Optional output CSV path relative to LOCAL_FILES_ROOT, including "
                    "the .csv filename. Use this when the user asks for an audit "
                    "matrix file or a Grist import. The parent folder must exist."
                ),
            },
        },
        "required": ["audit_relative_path", "client_directory"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        root: Path,
        summarizer: LocalFilesSummarizePdfAgent,
        *,
        api_key: str | None,
        base_url: str,
        requested_model: str | None,
        max_read_bytes: int,
        max_text_characters: int,
        max_files: int,
        max_total_pages: int,
        max_create_bytes: int = 5 * 1024 * 1024,
        batch_summarizer: LocalFilesSummarizePdfsAgent | None = None,
        artifact_store: MemoryArtifactStore = memory_artifact_store,
        client: Any | None = None,
        model: str | None = None,
    ) -> None:
        self.root = root
        self.summarizer = summarizer
        self.api_key = api_key
        self.base_url = base_url
        self.requested_model = requested_model
        self.max_read_bytes = max_read_bytes
        self.max_text_characters = max_text_characters
        self.max_files = max_files
        self.max_total_pages = max_total_pages
        self.max_create_bytes = max_create_bytes
        self.batch_summarizer = batch_summarizer
        self.artifact_store = artifact_store
        self._client = client
        self._model = model

    def _model_runtime(self) -> tuple[Any, str]:
        if self._client is not None and self._model is not None:
            return self._client, self._model
        if not self.api_key:
            raise AlbertAPIError("Set ALBERT_API_KEY before auditing a client folder")
        if self._client is None:
            self._client = AlbertClient(self.api_key, base_url=self.base_url)
        if self._model is None:
            self._model = self._client.resolve_model(self.requested_model)
        return self._client, self._model

    async def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        audit_path = arguments.get("audit_relative_path")
        client_directory = arguments.get("client_directory")
        focus = arguments.get("focus")
        recursive = arguments.get("recursive", True)
        max_depth = arguments.get("max_depth", 5)
        csv_relative_path = arguments.get("csv_relative_path")
        if not isinstance(audit_path, str) or not isinstance(client_directory, str):
            raise LocalFilesError(
                "audit_relative_path and client_directory must be strings"
            )
        if focus is not None and not isinstance(focus, str):
            raise LocalFilesError("focus must be a string")
        if not isinstance(recursive, bool):
            raise LocalFilesError("recursive must be a boolean")
        if not isinstance(max_depth, int) or isinstance(max_depth, bool):
            raise LocalFilesError("max_depth must be an integer")
        if not 0 <= max_depth <= 5:
            raise LocalFilesError("max_depth must be between 0 and 5")
        if csv_relative_path is not None and not isinstance(csv_relative_path, str):
            raise LocalFilesError("csv_relative_path must be a string")

        prepared = False
        memory = find_pdf_memory(self.root, source_relative_path=audit_path)
        if memory is None or not memory["up_to_date"]:
            await self.summarizer.summarize(audit_path)
            prepared = True

        client_memories: dict[str, Any] | None = None
        if self.batch_summarizer is not None:
            client_memories = await self.batch_summarizer.execute(
                {
                    "directory": client_directory,
                    "recursive": recursive,
                    "max_depth": max_depth,
                    "refresh": False,
                },
                context,
            )

        client, model = self._model_runtime()
        result = await audit_folder_against_reference(
            self.root,
            audit_relative_path=audit_path,
            client_directory=client_directory,
            focus=focus,
            client=client,
            model=model,
            max_read_bytes=self.max_read_bytes,
            max_text_characters=self.max_text_characters,
            max_files=self.max_files,
            max_total_pages=self.max_total_pages,
            recursive=recursive,
            max_depth=max_depth,
        )
        result["reference_prepared"] = prepared
        if csv_relative_path is not None:
            normalized_csv_path = csv_relative_path.strip().replace("\\", "/")
            output_path = Path(normalized_csv_path)
            if (
                not normalized_csv_path
                or output_path.is_absolute()
                or output_path.suffix.lower() != ".csv"
                or output_path.name in {"", ".", ".."}
            ):
                raise LocalFilesError(
                    "csv_relative_path must be a relative path ending in .csv"
                )
            stream = io.StringIO(newline="")
            writer = csv.writer(stream)
            writer.writerow(
                [
                    "criterion",
                    "requirement",
                    "verdict",
                    "reference evidence",
                    "client evidence",
                    "reasoning",
                    "corrective action",
                ]
            )
            for finding in result["findings"]:
                writer.writerow(
                    [
                        finding["name"],
                        finding["requirement"],
                        finding["status"],
                        finding["reference_evidence"],
                        finding["client_evidence"],
                        finding["reasoning"],
                        finding["corrective_action"],
                    ]
                )
            created_csv = create_local_text_file(
                self.root,
                directory=output_path.parent.as_posix(),
                file_name=output_path.stem,
                extension="csv",
                content=stream.getvalue(),
                max_bytes=self.max_create_bytes,
            )
            result["audit_csv"] = created_csv
        audit_payload = {
            "audit": result.pop("audit"),
            "criteria": result.pop("criteria"),
            "findings": result.pop("findings"),
            "sources": result.pop("sources"),
            "audit_reference": result["audit_reference"],
            "client_directory": result["client_directory"],
            "overall_result": result["overall_result"],
            "complete": result["complete"],
            "limitations": list(result["limitations"]),
        }
        verdict_counts: dict[str, int] = {}
        for finding in audit_payload["findings"]:
            verdict = str(finding["status"])
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
        audit_payload["verdict_counts"] = verdict_counts
        audit_artifact = self.artifact_store.put(
            audit_payload,
            kind="audit_report",
            media_type="application/vnd.lasuite.audit+json",
            name=f"Audit of {result['client_directory']}",
            metadata={
                "criteria_count": result["criteria_count"],
                "source_count": result["source_count"],
                "complete": result["complete"],
            },
        )
        result["verdict_counts"] = verdict_counts
        result["audit_artifact"] = audit_artifact.tool_value()
        if client_memories is not None:
            result["client_memories"] = {
                key: client_memories[key]
                for key in (
                    "requested",
                    "created",
                    "updated",
                    "skipped",
                    "failed",
                    "limited",
                    "limitation",
                )
            }
            result["client_memories_complete"] = (
                not client_memories["limited"] and client_memories["failed"] == 0
            )
        return result
