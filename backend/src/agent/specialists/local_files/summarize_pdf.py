"""Create a durable Markdown memory from an entire local PDF."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import AlbertAPIError, LocalFilesError, PdfError
from providers.albert import AlbertClient
from services.local_files import read_local_pdf, resolve_local_file
from services.pdf import extract_pdf_pages
from services.pdf_memory import save_pdf_memory, summarize_pdf_pages


class LocalFilesSummarizePdfAgent(SpecialistAgent):
    name = "local_files_summarize_pdf"
    description = (
        "Read every extractable page of one local PDF and create or refresh a durable, "
        "page-cited Markdown summary under LOCAL_FILES_ROOT/memory. The memory includes "
        "a link to the original PDF and a comprehensive topic/page guide for future "
        "questions. Use this when the user asks to remember, index, fully summarize, "
        "or prepare a PDF for later questions."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "relative_path": {
                "type": "string",
                "description": (
                    "PDF path relative to LOCAL_FILES_ROOT, exactly as returned by "
                    "local_files_list_items."
                ),
            }
        },
        "required": ["relative_path"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        root: Path,
        *,
        api_key: str | None,
        base_url: str,
        requested_model: str | None,
        max_read_bytes: int,
        max_pages: int,
        client: Any | None = None,
        model: str | None = None,
    ) -> None:
        self.root = root
        self.api_key = api_key
        self.base_url = base_url
        self.requested_model = requested_model
        self.max_read_bytes = max_read_bytes
        self.max_pages = max_pages
        self._client = client
        self._model = model

    def _model_runtime(self) -> tuple[Any, str]:
        if self._client is not None and self._model is not None:
            return self._client, self._model
        if not self.api_key:
            raise AlbertAPIError("Set ALBERT_API_KEY before summarizing a PDF")
        if self._client is None:
            self._client = AlbertClient(self.api_key, base_url=self.base_url)
        if self._model is None:
            self._model = self._client.resolve_model(self.requested_model)
        return self._client, self._model

    async def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        relative_path = arguments.get("relative_path")
        if not isinstance(relative_path, str):
            raise LocalFilesError("relative_path must be a string")
        return await self.summarize(relative_path)

    async def summarize(self, relative_path: str) -> dict[str, Any]:
        """Create or refresh one memory; shared with the bounded batch agent."""
        source = resolve_local_file(self.root, relative_path)
        pdf_bytes = read_local_pdf(
            self.root,
            relative_path,
            max_bytes=self.max_read_bytes,
        )
        pages = extract_pdf_pages(pdf_bytes)
        if len(pages) > self.max_pages:
            raise PdfError(
                f"The PDF has {len(pages)} pages; the configured complete-summary "
                f"limit is {self.max_pages} pages"
            )
        client, model = self._model_runtime()
        title, markdown, model_calls = await summarize_pdf_pages(
            pages,
            source_name=source.name,
            client=client,
            model=model,
        )
        result = save_pdf_memory(
            self.root,
            source_relative_path=relative_path,
            title=title,
            summary_markdown=markdown,
            total_pages=len(pages),
        )
        result.update(
            {
                "pages_analyzed": len(pages),
                "complete": True,
                "model_calls": model_calls,
            }
        )
        return result
