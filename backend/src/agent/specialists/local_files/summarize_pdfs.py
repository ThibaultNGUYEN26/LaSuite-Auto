"""Create independent Markdown memories for a bounded batch of local PDFs."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import AgentError, LocalFilesError
from agent.specialists.local_files.summarize_pdf import LocalFilesSummarizePdfAgent
from services.local_files import list_local_items, resolve_local_file
from services.pdf_memory import find_pdf_memory


class LocalFilesSummarizePdfsAgent(SpecialistAgent):
    name = "local_files_summarize_pdfs"
    description = (
        "Privately prepare every PDF from one or several bounded local folders, or "
        "from an explicit path list, in one operation. Use automatically when the "
        "user asks to analyze several folders or documents. Each document is analyzed "
        "independently. Up-to-date memories are reused and only PDFs whose content "
        "changed are regenerated. One failure does not stop the remaining files."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "relative_paths": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 50,
                "uniqueItems": True,
                "description": "Explicit PDF paths relative to LOCAL_FILES_ROOT.",
            },
            "directory": {
                "type": "string",
                "description": (
                    "Folder relative to LOCAL_FILES_ROOT. Use this instead of "
                    "relative_paths to discover PDFs automatically."
                ),
            },
            "directories": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 10,
                "uniqueItems": True,
                "description": (
                    "Several folders relative to LOCAL_FILES_ROOT. Use this to "
                    "prepare PDFs from multiple folders in one operation."
                ),
            },
            "recursive": {"type": "boolean", "description": "Defaults to true."},
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "description": "Maximum folder depth. Defaults to 5.",
            },
        },
        "oneOf": [
            {"required": ["relative_paths"]},
            {"required": ["directory"]},
            {"required": ["directories"]},
        ],
        "additionalProperties": False,
    }

    def __init__(
        self,
        root: Path,
        summarizer: LocalFilesSummarizePdfAgent,
        *,
        max_files: int = 20,
        concurrency: int = 2,
    ) -> None:
        if max_files < 1:
            raise ValueError("max_files must be positive")
        if concurrency < 1:
            raise ValueError("concurrency must be positive")
        self.root = root
        self.summarizer = summarizer
        self.max_files = max_files
        self.concurrency = concurrency

    def _paths(self, arguments: dict[str, Any]) -> tuple[list[str], bool, str | None]:
        relative_paths = arguments.get("relative_paths")
        directory = arguments.get("directory")
        directories = arguments.get("directories")
        if sum(value is not None for value in (relative_paths, directory, directories)) > 1:
            raise LocalFilesError(
                "Provide relative_paths, directory, or directories, not several"
            )
        if relative_paths is not None:
            if (
                not isinstance(relative_paths, list)
                or not relative_paths
                or not all(isinstance(path, str) for path in relative_paths)
            ):
                raise LocalFilesError(
                    "relative_paths must be a non-empty array of strings"
                )
            paths = list(dict.fromkeys(relative_paths))
            for relative_path in paths:
                if resolve_local_file(self.root, relative_path).suffix.lower() != ".pdf":
                    raise LocalFilesError("Every relative_paths item must be a PDF")
            limited = len(paths) > self.max_files
            return paths[: self.max_files], limited, (
                f"Only the first {self.max_files} requested PDFs were processed."
                if limited
                else None
            )

        if directories is not None:
            if (
                not isinstance(directories, list)
                or not directories
                or len(directories) > 10
                or not all(
                    isinstance(value, str) and value.strip()
                    for value in directories
                )
            ):
                raise LocalFilesError(
                    "directories must be an array of one to ten folder paths"
                )
            selected_directories = list(dict.fromkeys(directories))
        elif isinstance(directory, str) and directory.strip():
            selected_directories = [directory]
        else:
            raise LocalFilesError(
                "Provide relative_paths, directory, or directories"
            )
        recursive = arguments.get("recursive", True)
        if not isinstance(recursive, bool):
            raise LocalFilesError("recursive must be a boolean")
        max_depth = arguments.get("max_depth", 5)
        if not isinstance(max_depth, int) or isinstance(max_depth, bool):
            raise LocalFilesError("max_depth must be an integer")
        discovered: list[str] = []
        listings_complete = True
        for selected_directory in selected_directories:
            listing = list_local_items(
                self.root,
                directory=selected_directory,
                limit=500,
                recursive=recursive,
                max_depth=max_depth,
            )
            listings_complete = listings_complete and listing["complete"]
            discovered.extend(
                item["relative_path"]
                for item in listing["items"]
                if item.get("type") == "file" and item.get("extension") == ".pdf"
            )
        discovered = list(dict.fromkeys(discovered))
        limited = len(discovered) > self.max_files or not listings_complete
        limitation = None
        if limited:
            limitation = (
                f"Only the first {self.max_files} discovered PDFs were processed, or "
                "some nested files were outside the bounded folder scan."
            )
        return discovered[: self.max_files], limited, limitation

    async def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        paths, limited, limitation = self._paths(arguments)
        if not paths:
            return {
                "status": "completed",
                "requested": 0,
                "created": 0,
                "updated": 0,
                "skipped": 0,
                "failed": 0,
                "limited": limited,
                "limitation": limitation,
                "results": [],
            }

        semaphore = asyncio.Semaphore(self.concurrency)

        async def process(relative_path: str) -> dict[str, Any]:
            existing = find_pdf_memory(
                self.root,
                source_relative_path=relative_path,
            )
            if existing and existing["up_to_date"]:
                return {
                    "status": "skipped",
                    "reason": "up_to_date",
                    "source_relative_path": relative_path,
                    "relative_path": existing["relative_path"],
                    "title": existing["title"],
                }
            try:
                async with semaphore:
                    return await self.summarizer.summarize(relative_path)
            except AgentError as exc:
                return {
                    "status": "failed",
                    "source_relative_path": relative_path,
                    "error": str(exc),
                }

        results = list(await asyncio.gather(*(process(path) for path in paths)))
        return {
            "status": "completed",
            "requested": len(paths),
            "created": sum(item["status"] == "created" for item in results),
            "updated": sum(item["status"] == "updated" for item in results),
            "skipped": sum(item["status"] == "skipped" for item in results),
            "failed": sum(item["status"] == "failed" for item in results),
            "limited": limited,
            "limitation": limitation,
            "results": results,
        }
