"""Analyze every supported document in one local folder as a bounded corpus."""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import AlbertAPIError, LocalFilesError, PdfError
from agent.specialists.local_files.summarize_pdfs import LocalFilesSummarizePdfsAgent
from providers.albert import AlbertClient
from services.local_files import list_local_items, read_local_text, resolve_local_file
from services.pdf_audit import TEXT_EVIDENCE_EXTENSIONS
from services.pdf_memory import complete_text, load_pdf_memory

ANALYSIS_BATCH_SIZE = 5
ANALYSIS_CONCURRENCY = 2
DOCUMENT_ANALYSIS_PROMPT = (
    "Summarize each supplied document independently. This is descriptive document "
    "analysis, not an audit: do not compare documents, assign compliance verdicts, "
    "or infer missing facts. Return only JSON as {\"documents\":[...]}. Return exactly "
    "one entry per supplied path with path, summary (two to five useful sentences), "
    "and key_points (an array of up to five short strings). Every factual PDF summary "
    "must retain [p. N] or [pp. N-M] citations. Every factual text/CSV summary must "
    "retain the supplied [path, lines X-Y] citation. Do not return uncited claims."
)


def _parse_document_summaries(
    raw: str, expected_paths: set[str]
) -> dict[str, dict[str, Any]]:
    start, end = raw.find("{"), raw.rfind("}")
    try:
        payload = json.loads(raw[start : end + 1])
    except (json.JSONDecodeError, TypeError):
        return {}
    values = payload.get("documents") if isinstance(payload, dict) else None
    if not isinstance(values, list):
        return {}
    parsed: dict[str, dict[str, Any]] = {}
    for value in values:
        if not isinstance(value, dict) or value.get("path") not in expected_paths:
            continue
        path = value["path"]
        summary = value.get("summary")
        key_points = value.get("key_points")
        if not isinstance(summary, str) or not summary.strip():
            continue
        if not isinstance(key_points, list):
            key_points = []
        parsed[path] = {
            "summary": summary.strip(),
            "key_points": [
                point.strip()
                for point in key_points[:5]
                if isinstance(point, str) and point.strip()
            ],
        }
    return parsed


def _has_source_citation(path: str, summary: dict[str, Any]) -> bool:
    combined = " ".join([summary["summary"], *summary["key_points"]])
    if Path(path).suffix.lower() == ".pdf":
        return re.search(r"\[(?:p|pp)\.\s*\d+", combined) is not None
    return "lines " in combined and path in combined


class LocalFilesAnalyzeFolderAgent(SpecialistAgent):
    name = "local_files_analyze_folder"
    description = (
        "Analyze and separately summarize every supported PDF, CSV, and text document "
        "in one selected local folder in a single bounded operation. Use this for a "
        "general request to analyze, understand, review, or prepare a client corpus; "
        "do not use an audit capability unless the user explicitly asks for an audit, "
        "compliance assessment, or comparison against requirements. It automatically "
        "creates reusable memories for all PDFs. additional_pdf_paths can include a "
        "separate reference PDF such as a checklist without comparing it to the folder. "
        "When a README identifies the in-scope client container, select the client from "
        "that container rather than an unrelated similarly named folder."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "Exact document folder relative to LOCAL_FILES_ROOT.",
            },
            "additional_pdf_paths": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": 10,
                "uniqueItems": True,
                "description": "Separate PDFs to analyze alongside, but not compare with, the folder.",
            },
            "focus": {
                "type": "string",
                "description": "Optional descriptive-analysis focus.",
            },
            "recursive": {"type": "boolean", "default": True},
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "default": 5,
            },
        },
        "required": ["directory"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        root: Path,
        batch_summarizer: LocalFilesSummarizePdfsAgent,
        *,
        api_key: str | None,
        base_url: str,
        requested_model: str | None,
        max_read_bytes: int,
        max_text_characters: int,
        max_files: int,
        client: Any | None = None,
        model: str | None = None,
    ) -> None:
        self.root = root
        self.batch_summarizer = batch_summarizer
        self.api_key = api_key
        self.base_url = base_url
        self.requested_model = requested_model
        self.max_read_bytes = max_read_bytes
        self.max_text_characters = max_text_characters
        self.max_files = max_files
        self._client = client
        self._model = model

    def _model_runtime(self) -> tuple[Any, str]:
        if self._client is not None and self._model is not None:
            return self._client, self._model
        if not self.api_key:
            raise AlbertAPIError("Set ALBERT_API_KEY before analyzing a document folder")
        if self._client is None:
            self._client = AlbertClient(self.api_key, base_url=self.base_url)
        if self._model is None:
            self._model = self._client.resolve_model(self.requested_model)
        return self._client, self._model

    async def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        directory = arguments.get("directory")
        additional_paths = arguments.get("additional_pdf_paths", [])
        focus = arguments.get("focus")
        recursive = arguments.get("recursive", True)
        max_depth = arguments.get("max_depth", 5)
        if not isinstance(directory, str) or not directory.strip():
            raise LocalFilesError("directory must be a non-empty string")
        if (
            not isinstance(additional_paths, list)
            or len(additional_paths) > 10
            or not all(isinstance(path, str) for path in additional_paths)
        ):
            raise LocalFilesError("additional_pdf_paths must be an array of PDF paths")
        if focus is not None and not isinstance(focus, str):
            raise LocalFilesError("focus must be a string")
        if not isinstance(recursive, bool):
            raise LocalFilesError("recursive must be a boolean")
        if not isinstance(max_depth, int) or isinstance(max_depth, bool) or not 0 <= max_depth <= 5:
            raise LocalFilesError("max_depth must be between 0 and 5")

        listing = list_local_items(
            self.root,
            directory=directory,
            limit=500,
            recursive=recursive,
            max_depth=max_depth,
        )
        paths = [
            item["relative_path"]
            for item in listing["items"]
            if item["type"] == "file"
            and (item["extension"] == ".pdf" or item["extension"] in TEXT_EVIDENCE_EXTENSIONS)
        ]
        for path in additional_paths:
            if resolve_local_file(self.root, path).suffix.lower() != ".pdf":
                raise LocalFilesError("Every additional_pdf_paths item must be a PDF")
        paths = list(dict.fromkeys([*additional_paths, *paths]))
        if not paths:
            raise LocalFilesError("The selected folder contains no supported documents")

        limitations: list[str] = []
        if not listing["complete"] and listing.get("limitation"):
            limitations.append(str(listing["limitation"]))
        if len(paths) > self.max_files:
            limitations.append(f"Only the first {self.max_files} supported documents were analyzed.")
            paths = paths[: self.max_files]
        pdf_paths = [path for path in paths if Path(path).suffix.lower() == ".pdf"]
        text_paths = [path for path in paths if Path(path).suffix.lower() != ".pdf"]

        memory_result = await self.batch_summarizer.execute(
            {"relative_paths": pdf_paths, "refresh": False}, context
        ) if pdf_paths else {
            "requested": 0, "created": 0, "updated": 0, "skipped": 0,
            "failed": 0, "limited": False, "limitation": None,
        }
        if memory_result["limited"] and memory_result.get("limitation"):
            limitations.append(str(memory_result["limitation"]))

        materials: dict[str, str] = {}
        for path in pdf_paths:
            try:
                memory = load_pdf_memory(self.root, source_relative_path=path)
            except (LocalFilesError, PdfError, OSError) as exc:
                limitations.append(f"Could not load the analysis for `{path}`: {exc}")
                continue
            if memory is None or not memory["up_to_date"]:
                limitations.append(f"No complete PDF analysis was available for `{path}`.")
                continue
            materials[path] = memory["content"][:12_000]

        for path in text_paths:
            try:
                text_result = read_local_text(
                    self.root,
                    path,
                    max_bytes=self.max_read_bytes,
                    max_characters=self.max_text_characters,
                )
            except (LocalFilesError, OSError) as exc:
                limitations.append(f"Could not read `{path}`: {exc}")
                continue
            returned = text_result["content"][:12_000]
            line_count = max(len(returned.splitlines()), 1)
            materials[path] = (
                f"[{path}, lines 1-{line_count}]\n{returned}"
            )
            if text_result["truncated"]:
                limitations.append(f"Only part of `{path}` could be analyzed.")

        client, model = self._model_runtime()
        material_paths = list(materials)
        batches = [
            material_paths[start : start + ANALYSIS_BATCH_SIZE]
            for start in range(0, len(material_paths), ANALYSIS_BATCH_SIZE)
        ]
        semaphore = asyncio.Semaphore(ANALYSIS_CONCURRENCY)

        async def analyze_batch(batch: list[str]) -> tuple[dict[str, dict[str, Any]], int]:
            content = f"Focus: {focus or 'General descriptive analysis'}\n\n" + "\n\n---\n\n".join(
                f"DOCUMENT PATH: {path}\n{materials[path]}" for path in batch
            )
            async with semaphore:
                raw = await complete_text(
                    client, model=model, system=DOCUMENT_ANALYSIS_PROMPT, content=content
                )
                parsed = _parse_document_summaries(raw, set(batch))
                parsed = {
                    path: summary
                    for path, summary in parsed.items()
                    if _has_source_citation(path, summary)
                }
                calls = 1
                if set(parsed) != set(batch):
                    raw = await complete_text(
                        client,
                        model=model,
                        system=DOCUMENT_ANALYSIS_PROMPT,
                        content="Return every supplied path exactly once.\n\n" + content,
                    )
                    parsed = _parse_document_summaries(raw, set(batch))
                    parsed = {
                        path: summary
                        for path, summary in parsed.items()
                        if _has_source_citation(path, summary)
                    }
                    calls += 1
            return parsed, calls

        results = await asyncio.gather(*(analyze_batch(batch) for batch in batches))
        summaries: dict[str, dict[str, Any]] = {}
        model_calls = 0
        for parsed, calls in results:
            summaries.update(parsed)
            model_calls += calls

        missing = [path for path in material_paths if path not in summaries]
        for path in missing:
            summaries[path] = {
                "summary": "A reliable concise summary could not be generated in this run.",
                "key_points": [],
            }
            limitations.append(f"The concise summary for `{path}` could not be generated reliably.")

        report = [f"# Document analysis — {directory}", ""]
        for path in material_paths:
            summary = summaries[path]
            report.extend([f"## {path}", "", summary["summary"], ""])
            report.extend(f"- {point}" for point in summary["key_points"])
            report.append("")
        if limitations:
            report.extend(["## Limitations", ""])
            report.extend(f"- {limitation}" for limitation in limitations)

        return {
            "status": "analyzed",
            "directory": directory,
            "document_count": len(material_paths),
            "pdf_count": sum(path in materials for path in pdf_paths),
            "text_count": sum(path in materials for path in text_paths),
            "analysis": "\n".join(report).strip(),
            "complete": not limitations,
            "limitations": limitations,
            "pdf_memories": {
                key: memory_result[key]
                for key in ("requested", "created", "updated", "skipped", "failed", "limited")
            },
            "model_calls": model_calls,
        }
