"""Search relevant pages across a bounded local PDF corpus."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import LocalFilesError
from services.local_files import list_local_items, read_local_pdf, resolve_local_file
from services.pdf_search import PdfSource, search_pdf_sources


class LocalFilesSearchPdfsAgent(SpecialistAgent):
    name = "local_files_search_pdfs"
    description = (
        "Search inside many local PDF files for passages that answer a question. "
        "Use this instead of reading one PDF from the beginning when the user asks "
        "which document contains an answer, asks a question across a folder of PDFs, "
        "or follows up about information beyond an earlier excerpt. Returns grounded "
        "excerpts with filename and page citations."
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
            "directory": {
                "type": "string",
                "description": (
                    "Directory relative to the configured local root, such as "
                    "Downloads. Defaults to the root."
                ),
            },
            "recursive": {"type": "boolean", "description": "Defaults to true."},
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "description": "Maximum folder depth to search. Defaults to 5.",
            },
            "max_files": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "description": "Maximum PDFs to inspect.",
            },
            "top_k": {
                "type": "integer",
                "minimum": 1,
                "maximum": 20,
                "description": "Maximum relevant passages to return. Defaults to 8.",
            },
            "relative_paths": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": 20,
                "description": (
                    "Optional PDF paths returned by local_files_search_pdf_memory. "
                    "When supplied, search only these original PDFs."
                ),
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        root: Path,
        *,
        max_read_bytes: int,
        max_files: int = 50,
        max_total_pages: int = 2_000,
    ) -> None:
        self.root = root
        self.max_read_bytes = max_read_bytes
        self.max_files = max_files
        self.max_total_pages = max_total_pages

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip():
            raise LocalFilesError("query must be a non-empty string")
        directory = arguments.get("directory", ".")
        if not isinstance(directory, str):
            raise LocalFilesError("directory must be a string")
        recursive = arguments.get("recursive", True)
        if not isinstance(recursive, bool):
            raise LocalFilesError("recursive must be a boolean")
        max_depth = arguments.get("max_depth", 5)
        if not isinstance(max_depth, int) or isinstance(max_depth, bool):
            raise LocalFilesError("max_depth must be an integer")
        requested_max_files = arguments.get("max_files", self.max_files)
        if not isinstance(requested_max_files, int) or isinstance(
            requested_max_files, bool
        ):
            raise LocalFilesError("max_files must be an integer")
        max_files = min(requested_max_files, self.max_files)
        if max_files < 1:
            raise LocalFilesError("max_files must be positive")
        top_k = arguments.get("top_k", 8)
        if not isinstance(top_k, int) or isinstance(top_k, bool):
            raise LocalFilesError("top_k must be an integer")

        relative_paths = arguments.get("relative_paths")
        if relative_paths is not None and (
            not isinstance(relative_paths, list)
            or not relative_paths
            or not all(isinstance(path, str) for path in relative_paths)
        ):
            raise LocalFilesError("relative_paths must be a non-empty array of strings")

        if relative_paths is not None:
            resolved_root = self.root.expanduser().resolve()
            pdf_items = []
            for relative_path in dict.fromkeys(relative_paths):
                path = resolve_local_file(self.root, relative_path)
                if path.suffix.lower() != ".pdf":
                    raise LocalFilesError("Every relative_paths item must be a PDF")
                stat = path.stat()
                pdf_items.append(
                    {
                        "name": path.name,
                        "type": "file",
                        "relative_path": path.relative_to(resolved_root).as_posix(),
                        "extension": ".pdf",
                        "size": stat.st_size,
                        "modified_at": str(stat.st_mtime_ns),
                    }
                )
            listing_complete = True
        else:
            listing = list_local_items(
                self.root,
                directory=directory,
                limit=500,
                recursive=recursive,
                max_depth=max_depth,
            )
            pdf_items = [
                item
                for item in listing["items"]
                if item.get("type") == "file" and item.get("extension") == ".pdf"
            ]
            listing_complete = listing["complete"]
        selected_items = pdf_items[:max_files]
        sources = [
            PdfSource(
                cache_key=(
                    f"local:{item['relative_path']}:{item.get('modified_at')}:"
                    f"{item.get('size')}"
                ),
                name=item["name"],
                reference=item["relative_path"],
                load=lambda relative_path=item["relative_path"]: read_local_pdf(
                    self.root,
                    relative_path,
                    max_bytes=self.max_read_bytes,
                ),
            )
            for item in selected_items
        ]
        result = search_pdf_sources(
            sources,
            query=query,
            top_k=top_k,
            max_total_pages=self.max_total_pages,
        )
        source_limited = len(pdf_items) > len(selected_items) or not listing_complete
        result.update(
            {
                "location": "local",
                "directory": directory,
                "pdfs_discovered": len(pdf_items),
                "source_limited": source_limited,
                "source_limitation": (
                    "Some files or folders were outside this bounded search. Narrow "
                    "the folder or request a larger search if no answer was found."
                    if source_limited
                    else None
                ),
            }
        )
        result["corpus_limited"] = result["corpus_limited"] or source_limited
        return result
