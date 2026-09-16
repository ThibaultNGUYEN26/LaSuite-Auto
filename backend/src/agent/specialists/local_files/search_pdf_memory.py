"""Search durable local PDF memories before querying original documents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError
from services.pdf_memory import search_pdf_memories


class LocalFilesSearchPdfMemoryAgent(SpecialistAgent):
    name = "local_files_search_pdf_memory"
    description = (
        "Search Markdown PDF memories under LOCAL_FILES_ROOT/memory to identify which "
        "original local PDF and page topics are relevant to a question. Use this first "
        "when the user asks a question across remembered PDFs, then search the returned "
        "source_relative_path in the original PDF for final evidence."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "top_k": {"type": "integer", "minimum": 1, "maximum": 20},
        },
        "required": ["query"],
        "additionalProperties": False,
    }

    def __init__(self, root: Path) -> None:
        self.root = root

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip():
            raise LocalFilesError("query must be a non-empty string")
        top_k = arguments.get("top_k", 5)
        if not isinstance(top_k, int) or isinstance(top_k, bool):
            raise LocalFilesError("top_k must be an integer")
        return search_pdf_memories(self.root, query=query, top_k=top_k)
