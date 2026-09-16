"""Search relevant pages across a bounded Drive PDF corpus."""

from __future__ import annotations

from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import download_drive_pdf, list_drive_items
from services.pdf_search import PdfSource, search_pdf_sources


class DriveSearchPdfsAgent(SpecialistAgent):
    name = "drive_search_pdfs"
    description = (
        "Search inside many La Suite Drive PDF files for passages that answer a "
        "question. Use this instead of reading one PDF from the beginning when the "
        "user asks which Drive document contains an answer or asks a question across "
        "a PDF collection. Returns grounded excerpts with filename and page citations."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Retrieval query using the user's core subject terms and useful "
                    "synonyms likely to appear in the documents."
                ),
            },
            "folder_id": {
                "type": "string",
                "format": "uuid",
                "description": "Optional Drive folder to search. Defaults to My files.",
            },
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "description": "Maximum folder depth to search. Defaults to 5.",
            },
            "max_files": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50,
                "description": "Maximum PDFs to download and inspect.",
            },
            "top_k": {
                "type": "integer",
                "minimum": 1,
                "maximum": 20,
                "description": "Maximum relevant passages to return. Defaults to 8.",
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        base_url: str,
        session_id: str | None,
        *,
        max_download_bytes: int,
        max_files: int = 20,
        max_total_pages: int = 2_000,
    ) -> None:
        self.base_url = base_url
        self.session_id = session_id
        self.max_download_bytes = max_download_bytes
        self.max_files = max_files
        self.max_total_pages = max_total_pages

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip():
            raise DriveAPIError("query must be a non-empty string")
        folder_id = arguments.get("folder_id")
        if folder_id is not None and not isinstance(folder_id, str):
            raise DriveAPIError("folder_id must be a string")
        max_depth = arguments.get("max_depth", 5)
        if not isinstance(max_depth, int) or isinstance(max_depth, bool):
            raise DriveAPIError("max_depth must be an integer")
        requested_max_files = arguments.get("max_files", self.max_files)
        if not isinstance(requested_max_files, int) or isinstance(
            requested_max_files, bool
        ):
            raise DriveAPIError("max_files must be an integer")
        max_files = min(requested_max_files, self.max_files)
        if max_files < 1:
            raise DriveAPIError("max_files must be positive")
        top_k = arguments.get("top_k", 8)
        if not isinstance(top_k, int) or isinstance(top_k, bool):
            raise DriveAPIError("top_k must be an integer")

        listing = list_drive_items(
            self.base_url,
            self.session_id or "",
            limit=500,
            recursive=True,
            max_depth=max_depth,
            folder_id=folder_id,
        )
        pdf_items = []
        for item in listing["items"]:
            name = item.get("filename") or item.get("title") or "Untitled.pdf"
            media_type = item.get("mimetype")
            if item.get("type") == "folder" or not isinstance(item.get("id"), str):
                continue
            if media_type == "application/pdf" or str(name).lower().endswith(".pdf"):
                pdf_items.append((item, str(name)))

        selected_items = pdf_items[:max_files]
        sources = [
            PdfSource(
                cache_key=(
                    f"drive:{item['id']}:{item.get('updated_at')}:{item.get('size')}"
                ),
                name=name,
                reference=item["id"],
                load=lambda item_id=item["id"]: download_drive_pdf(
                    self.base_url,
                    self.session_id or "",
                    item_id,
                    max_bytes=self.max_download_bytes,
                ),
            )
            for item, name in selected_items
        ]
        result = search_pdf_sources(
            sources,
            query=query,
            top_k=top_k,
            max_total_pages=self.max_total_pages,
        )
        source_limited = len(pdf_items) > len(selected_items) or not listing["complete"]
        result.update(
            {
                "location": "drive",
                "folder_id": folder_id,
                "pdfs_discovered": len(pdf_items),
                "source_limited": source_limited,
                "source_limitation": (
                    "Some Drive files or folders were outside this bounded search. "
                    "Narrow the folder or request a larger search if no answer was found."
                    if source_limited
                    else None
                ),
            }
        )
        result["corpus_limited"] = result["corpus_limited"] or source_limited
        return result
