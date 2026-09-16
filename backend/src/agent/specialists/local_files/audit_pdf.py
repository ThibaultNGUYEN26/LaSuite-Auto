"""Audit one local client PDF against one local reference PDF."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import AlbertAPIError, LocalFilesError
from agent.specialists.local_files.summarize_pdf import LocalFilesSummarizePdfAgent
from providers.albert import AlbertClient
from services.pdf_audit import audit_pdf_against_reference
from services.pdf_memory import find_pdf_memory


class LocalFilesAuditPdfAgent(SpecialistAgent):
    name = "local_files_audit_pdf"
    description = (
        "Audit one local client PDF against one local audit/reference PDF. Use this "
        "only when the complete client evidence is a single PDF. For a client folder "
        "or multiple evidence documents, use the folder/corpus audit capability instead. "
        "The user does not need to request "
        "summaries or memories. Automatically prepares both documents, extracts the "
        "complete checklist, and reports a page-cited verdict and corrective action for "
        "every criterion. If the conversation already identifies the reference and "
        "client, proceed without asking the user to restate or confirm them."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "audit_relative_path": {
                "type": "string",
                "description": "Audit/reference PDF path relative to LOCAL_FILES_ROOT.",
            },
            "client_relative_path": {
                "type": "string",
                "description": "Client PDF path relative to LOCAL_FILES_ROOT.",
            },
            "focus": {
                "type": "string",
                "description": "Optional audit scope. Omit for every criterion.",
            },
        },
        "required": ["audit_relative_path", "client_relative_path"],
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
        max_total_pages: int,
        client: Any | None = None,
        model: str | None = None,
    ) -> None:
        self.root = root
        self.summarizer = summarizer
        self.api_key = api_key
        self.base_url = base_url
        self.requested_model = requested_model
        self.max_read_bytes = max_read_bytes
        self.max_total_pages = max_total_pages
        self._client = client
        self._model = model

    def _model_runtime(self) -> tuple[Any, str]:
        if self._client is not None and self._model is not None:
            return self._client, self._model
        if not self.api_key:
            raise AlbertAPIError("Set ALBERT_API_KEY before auditing PDFs")
        if self._client is None:
            self._client = AlbertClient(self.api_key, base_url=self.base_url)
        if self._model is None:
            self._model = self._client.resolve_model(self.requested_model)
        return self._client, self._model

    async def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        audit_path = arguments.get("audit_relative_path")
        client_path = arguments.get("client_relative_path")
        focus = arguments.get("focus")
        if not isinstance(audit_path, str) or not isinstance(client_path, str):
            raise LocalFilesError(
                "audit_relative_path and client_relative_path must be strings"
            )
        if audit_path == client_path:
            raise LocalFilesError(
                "The audit reference and client document must be different"
            )
        if focus is not None and not isinstance(focus, str):
            raise LocalFilesError("focus must be a string")

        prepared: list[str] = []

        async def ensure_memory(relative_path: str) -> None:
            memory = find_pdf_memory(self.root, source_relative_path=relative_path)
            if memory is None or not memory["up_to_date"]:
                await self.summarizer.summarize(relative_path)
                prepared.append(relative_path)

        await asyncio.gather(ensure_memory(audit_path), ensure_memory(client_path))
        client, model = self._model_runtime()
        result = await audit_pdf_against_reference(
            self.root,
            audit_relative_path=audit_path,
            client_relative_path=client_path,
            focus=focus,
            client=client,
            model=model,
            max_read_bytes=self.max_read_bytes,
            max_total_pages=self.max_total_pages,
        )
        result["documents_prepared"] = len(prepared)
        return result
