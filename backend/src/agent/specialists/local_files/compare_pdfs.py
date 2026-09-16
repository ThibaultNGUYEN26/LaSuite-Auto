"""Compare two local PDFs using their memories and original page evidence."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import AlbertAPIError, LocalFilesError
from agent.specialists.local_files.summarize_pdf import LocalFilesSummarizePdfAgent
from providers.albert import AlbertClient
from services.pdf_comparison import compare_pdf_memories
from services.pdf_memory import find_pdf_memory


class LocalFilesComparePdfsAgent(SpecialistAgent):
    name = "local_files_compare_pdfs"
    description = (
        "Compare exactly two local PDFs in depth. It automatically creates or refreshes "
        "each PDF's reusable memory, plans useful comparison dimensions, retrieves "
        "supporting pages from both original documents, and returns similarities, "
        "differences, contradictions, unique coverage, and exact page citations."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "relative_paths": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "maxItems": 2,
                "uniqueItems": True,
                "description": (
                    "Exactly two PDF paths relative to LOCAL_FILES_ROOT, as returned "
                    "by local_files_list_items."
                ),
            },
            "focus": {
                "type": "string",
                "description": (
                    "Optional comparison question or subject. Omit for a broad, "
                    "document-wide comparison."
                ),
            },
        },
        "required": ["relative_paths"],
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
            raise AlbertAPIError("Set ALBERT_API_KEY before comparing PDFs")
        if self._client is None:
            self._client = AlbertClient(self.api_key, base_url=self.base_url)
        if self._model is None:
            self._model = self._client.resolve_model(self.requested_model)
        return self._client, self._model

    async def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        relative_paths = arguments.get("relative_paths")
        focus = arguments.get("focus")
        if (
            not isinstance(relative_paths, list)
            or len(relative_paths) != 2
            or not all(isinstance(path, str) for path in relative_paths)
            or relative_paths[0] == relative_paths[1]
        ):
            raise LocalFilesError("relative_paths must contain two different PDF paths")
        if focus is not None and not isinstance(focus, str):
            raise LocalFilesError("focus must be a string")

        refreshed: list[str] = []

        async def ensure_memory(relative_path: str) -> None:
            memory = find_pdf_memory(
                self.root,
                source_relative_path=relative_path,
            )
            if memory is None or not memory["up_to_date"]:
                await self.summarizer.summarize(relative_path)
                refreshed.append(relative_path)

        await asyncio.gather(*(ensure_memory(path) for path in relative_paths))
        client, model = self._model_runtime()
        result = await compare_pdf_memories(
            self.root,
            relative_paths=relative_paths,
            focus=focus,
            client=client,
            model=model,
            max_read_bytes=self.max_read_bytes,
            max_total_pages=self.max_total_pages,
        )
        result["memories_created_or_refreshed"] = refreshed
        return result
