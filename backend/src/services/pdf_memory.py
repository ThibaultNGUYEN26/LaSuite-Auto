"""Create and search durable Markdown memories for local PDF documents."""

from __future__ import annotations

import asyncio
import json
import os
import re
import unicodedata
from collections import Counter
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import quote
from uuid import uuid4

from agent.artifacts import Artifact
from agent.errors import PdfError
from services.local_files import resolve_local_directory, resolve_local_file
from services.pdf_search import search_tokens

MEMORY_DIRECTORY = "memory"
METADATA_PREFIX = "<!-- auto-pdf-memory: "
MAP_INPUT_CHARACTERS = 42_000
REDUCE_INPUT_CHARACTERS = 48_000
SUMMARY_CONCURRENCY = 3

MAP_PROMPT = (
    "You create evidence-grounded notes for one portion of a PDF. Read every supplied "
    "page. Produce concise Markdown covering its subjects, important facts, named "
    "entities, definitions, recommendations, procedures, and conclusions. Preserve "
    "the page numbers using [p. N] citations. Include a compact topic-to-page map. "
    "Do not use outside knowledge and do not claim anything absent from the pages. "
    "Stay below 900 words."
)

REDUCE_PROMPT = (
    "Merge these partial PDF notes without losing distinct topics or page citations. "
    "Deduplicate repeated material, preserve useful details, and keep a comprehensive "
    "topic-to-page map. Use only the supplied notes. Return Markdown only and stay "
    "below 1,200 words."
)

FINAL_PROMPT = (
    "Create the durable memory for this PDF from the complete set of page-grounded "
    "notes. Return only JSON with exactly two string fields: title and markdown. "
    "The title must accurately name the document in 3 to 10 words and must not contain "
    "a filename extension. The markdown must not repeat the title as an H1. Organize it "
    "with these sections: Overview, Key points, Detailed topic and page guide, Questions "
    "this document can answer, and Limitations. Make the topic/page guide comprehensive "
    "enough to route future questions to the original PDF. Cite factual material with "
    "[p. N]. Use only the supplied notes and never invent unseen content."
)


class SummaryChatClient(Protocol):
    def chat_completion_stream(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> AsyncIterator[dict[str, Any]]: ...


async def complete_text(
    client: SummaryChatClient,
    *,
    model: str,
    system: str,
    content: str,
) -> str:
    parts: list[str] = []
    async for chunk in client.chat_completion_stream(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": content},
        ],
        tools=[],
    ):
        if chunk.get("type") == "content" and isinstance(chunk.get("delta"), str):
            parts.append(chunk["delta"])
    result = "".join(parts).strip()
    if not result:
        raise PdfError("The PDF summary model returned an empty response")
    return result


def _page_batches(pages: list[str]) -> list[str]:
    batches: list[str] = []
    current: list[str] = []
    current_size = 0
    for page_number, page_text in enumerate(pages, start=1):
        if not page_text.strip():
            continue
        offset = 0
        while offset < len(page_text):
            available = max(MAP_INPUT_CHARACTERS - 64, 1)
            segment = page_text[offset : offset + available]
            label = f"## Page {page_number}\n{segment}"
            separator_size = 2 if current else 0
            if current and current_size + separator_size + len(label) > MAP_INPUT_CHARACTERS:
                batches.append("\n\n".join(current))
                current = []
                current_size = 0
                separator_size = 0
            current.append(label)
            current_size += separator_size + len(label)
            offset += len(segment)
    if current:
        batches.append("\n\n".join(current))
    return batches


def _groups(values: list[str], max_characters: int) -> list[list[str]]:
    groups: list[list[str]] = []
    current: list[str] = []
    size = 0
    for value in values:
        if current and size + len(value) + 2 > max_characters:
            groups.append(current)
            current = []
            size = 0
        current.append(value)
        size += len(value) + 2
    if current:
        groups.append(current)
    return groups


def _parse_final(raw: str, *, fallback_title: str) -> tuple[str, str]:
    clean = raw.strip()
    if clean.startswith("```") and clean.endswith("```"):
        lines = clean.splitlines()
        clean = "\n".join(lines[1:-1]).strip()
    start, end = clean.find("{"), clean.rfind("}")
    try:
        payload = json.loads(clean[start : end + 1])
    except (json.JSONDecodeError, TypeError):
        return fallback_title, raw.strip()
    title = payload.get("title")
    markdown = payload.get("markdown")
    if not isinstance(title, str) or not title.strip():
        title = fallback_title
    if not isinstance(markdown, str) or not markdown.strip():
        markdown = raw.strip()
    return title.strip(), markdown.strip()


async def summarize_pdf_pages(
    pages: list[str],
    *,
    source_name: str,
    client: SummaryChatClient,
    model: str,
) -> tuple[str, str, int]:
    """Map every page into notes, recursively reduce, then synthesize a memory."""
    batches = _page_batches(pages)
    if not batches:
        raise PdfError("No extractable text was found in the PDF")

    semaphore = asyncio.Semaphore(SUMMARY_CONCURRENCY)

    async def summarize_part(system: str, content: str) -> str:
        async with semaphore:
            return await complete_text(
                client,
                model=model,
                system=system,
                content=content,
            )

    notes = list(
        await asyncio.gather(
            *(summarize_part(MAP_PROMPT, batch) for batch in batches)
        )
    )
    calls = len(notes)
    reduction_rounds = 0
    while sum(len(note) + 2 for note in notes) > REDUCE_INPUT_CHARACTERS:
        reduction_rounds += 1
        if reduction_rounds > 8:
            raise PdfError("The PDF notes could not be reduced to a safe summary size")
        reduced: list[str] = []
        groups = _groups(notes, REDUCE_INPUT_CHARACTERS)
        reduced.extend(
            await asyncio.gather(
                *(
                    summarize_part(
                        REDUCE_PROMPT,
                        "\n\n---\n\n".join(group),
                    )
                    for group in groups
                )
            )
        )
        calls += len(reduced)
        notes = reduced

    final = await complete_text(
        client,
        model=model,
        system=FINAL_PROMPT,
        content=(
            f"Source filename: {source_name}\n"
            f"Total PDF pages: {len(pages)}\n\n"
            + "\n\n---\n\n".join(notes)
        ),
    )
    calls += 1
    title, markdown = _parse_final(final, fallback_title=Path(source_name).stem)
    title = re.sub(r"\s+", " ", title).strip()[:160]
    if title.casefold().endswith(".pdf"):
        title = title[:-4].rstrip()
    return title, markdown, calls


def _slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = "".join(char for char in normalized if not unicodedata.combining(char))
    slug = re.sub(r"[^A-Za-z0-9]+", "-", ascii_value).strip("-").lower()
    return (slug[:80].rstrip("-") or "pdf-summary")


def _metadata_from_text(text: str) -> dict[str, Any] | None:
    first_line = text.splitlines()[0] if text else ""
    if not first_line.startswith(METADATA_PREFIX) or not first_line.endswith(" -->"):
        return None
    try:
        metadata = json.loads(first_line[len(METADATA_PREFIX) : -4])
    except json.JSONDecodeError:
        return None
    return metadata if isinstance(metadata, dict) else None


def _file_sha256(path: Path) -> str:
    """Hash a source document without loading the whole file into memory."""
    digest = sha256()
    try:
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise PdfError(f"Could not fingerprint the source PDF: {exc}") from exc
    return digest.hexdigest()


def _upgrade_legacy_fingerprint(
    path: Path,
    *,
    text: str,
    metadata: dict[str, Any],
    source_hash: str,
) -> None:
    """Add a hash to an old memory without regenerating its model-written summary."""
    metadata = {**metadata, "source_sha256": source_hash}
    first_newline = text.find("\n")
    remainder = text[first_newline:] if first_newline >= 0 else ""
    upgraded = (
        f"{METADATA_PREFIX}{json.dumps(metadata, ensure_ascii=False)} -->"
        f"{remainder}"
    )
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        temporary.write_text(upgraded, encoding="utf-8", newline="\n")
        temporary.replace(path)
    except OSError:
        # Cache migration must never prevent the existing memory from being reused.
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass


def find_pdf_memory(root: Path, *, source_relative_path: str) -> dict[str, Any] | None:
    """Return freshness information for a managed memory of one local PDF."""
    source = resolve_local_file(root, source_relative_path)
    resolved_root = resolve_local_directory(root)
    memory_directory = (resolved_root / MEMORY_DIRECTORY).resolve()
    try:
        memory_directory.relative_to(resolved_root)
    except ValueError as exc:
        raise PdfError("The memory directory escapes LOCAL_FILES_ROOT") from exc
    if not memory_directory.is_dir():
        return None

    source_stat = source.stat()
    for candidate in memory_directory.glob("*.md"):
        try:
            text = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        metadata = _metadata_from_text(text)
        if not metadata or metadata.get("source_path") != source_relative_path:
            continue
        stored_hash = metadata.get("source_sha256")
        if isinstance(stored_hash, str) and len(stored_hash) == 64:
            up_to_date = _file_sha256(source) == stored_hash
        else:
            # Memories created before content hashing was introduced remain usable.
            up_to_date = (
                metadata.get("source_size") == source_stat.st_size
                and metadata.get("source_mtime_ns") == source_stat.st_mtime_ns
            )
            if up_to_date:
                source_hash = _file_sha256(source)
                _upgrade_legacy_fingerprint(
                    candidate,
                    text=text,
                    metadata=metadata,
                    source_hash=source_hash,
                )
        return {
            "relative_path": candidate.relative_to(resolved_root).as_posix(),
            "source_relative_path": source_relative_path,
            "up_to_date": up_to_date,
            "total_pages": metadata.get("total_pages"),
            "title": next(
                (
                    line.removeprefix("# ").strip()
                    for line in text.splitlines()
                    if line.startswith("# ")
                ),
                candidate.stem,
            ),
        }
    return None


def load_pdf_memory(root: Path, *, source_relative_path: str) -> dict[str, Any] | None:
    """Load a managed memory and its freshness metadata for one source PDF."""
    found = find_pdf_memory(root, source_relative_path=source_relative_path)
    if found is None:
        return None
    resolved_root = resolve_local_directory(root)
    path = resolve_local_file(root, found["relative_path"])
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PdfError("Could not read the PDF memory") from exc
    sections = content.split("\n\n", 4)
    summary_markdown = sections[4].strip() if len(sections) == 5 else content.strip()
    return {**found, "content": content, "summary_markdown": summary_markdown}


def save_pdf_memory(
    root: Path,
    *,
    source_relative_path: str,
    title: str,
    summary_markdown: str,
    total_pages: int,
    source_sha256: str | None = None,
) -> dict[str, Any]:
    source = resolve_local_file(root, source_relative_path)
    resolved_root = resolve_local_directory(root)
    memory_directory = resolved_root / MEMORY_DIRECTORY
    memory_directory.mkdir(exist_ok=True)
    memory_directory = memory_directory.resolve()
    try:
        memory_directory.relative_to(resolved_root)
    except ValueError as exc:
        raise PdfError("The memory directory escapes LOCAL_FILES_ROOT") from exc

    existing = find_pdf_memory(root, source_relative_path=source_relative_path)
    existing_target = (
        resolved_root / existing["relative_path"] if existing is not None else None
    )

    target = existing_target or memory_directory / f"{_slug(title)}.md"
    if target.exists() and existing_target is None:
        suffix = sha256(source_relative_path.encode("utf-8")).hexdigest()[:8]
        target = memory_directory / f"{_slug(title)}-{suffix}.md"

    source_link = quote(os.path.relpath(source, memory_directory).replace("\\", "/"))
    stat = source.stat()
    metadata = {
        "type": "pdf_memory",
        "source_path": source_relative_path,
        "source_name": source.name,
        "source_size": stat.st_size,
        "source_mtime_ns": stat.st_mtime_ns,
        # A caller that already read the PDF can pass the hash of those exact bytes.
        # If the file changes during analysis, the saved memory is then immediately
        # considered stale instead of being associated with the newer file content.
        "source_sha256": source_sha256 or _file_sha256(source),
        "total_pages": total_pages,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    clean_markdown = summary_markdown.strip()
    clean_markdown = re.sub(r"^#\s+[^\n]+\n+", "", clean_markdown, count=1)
    document = (
        f"{METADATA_PREFIX}{json.dumps(metadata, ensure_ascii=False)} -->\n\n"
        f"# {title.strip()}\n\n"
        f"[Open the original PDF](<{source_link}>)\n\n"
        f"> Source: `{source_relative_path}` · {total_pages} pages\n\n"
        f"{clean_markdown}\n"
    )
    temporary = target.with_name(f".{target.name}.{uuid4().hex}.tmp")
    try:
        temporary.write_text(document, encoding="utf-8", newline="\n")
        temporary.replace(target)
    except OSError as exc:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise PdfError(f"Could not save the PDF memory: {exc}") from exc

    relative_path = target.relative_to(resolved_root).as_posix()
    return {
        "status": "created" if existing_target is None else "updated",
        "title": title.strip(),
        "relative_path": relative_path,
        "source_relative_path": source_relative_path,
        "total_pages": total_pages,
        "artifact": Artifact(
            kind="file",
            location="local",
            reference=relative_path,
            media_type="text/markdown",
            name=target.name,
            metadata={"source_path": source_relative_path, "document_type": "pdf_memory"},
        ).tool_value(),
    }


def search_pdf_memories(root: Path, *, query: str, top_k: int = 5) -> dict[str, Any]:
    """Find summary memories that can route a question to original PDFs."""
    if not query.strip():
        raise PdfError("query must be a non-empty string")
    if not 1 <= top_k <= 20:
        raise PdfError("top_k must be between 1 and 20")
    resolved_root = resolve_local_directory(root)
    memory_directory = resolved_root / MEMORY_DIRECTORY
    if not memory_directory.exists():
        return {"status": "searched", "query": query, "matches": [], "count": 0}
    memory_directory = memory_directory.resolve()
    try:
        memory_directory.relative_to(resolved_root)
    except ValueError as exc:
        raise PdfError("The memory directory escapes LOCAL_FILES_ROOT") from exc

    query_tokens = Counter(search_tokens(query))
    scored: list[tuple[float, dict[str, Any]]] = []
    for path in memory_directory.glob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        metadata = _metadata_from_text(text)
        if not metadata or not isinstance(metadata.get("source_path"), str):
            continue
        frequencies = Counter(search_tokens(text))
        score = sum(
            min(frequencies.get(token, 0), 4) * count
            for token, count in query_tokens.items()
        )
        if score <= 0:
            continue
        relative_path = path.relative_to(resolved_root).as_posix()
        scored.append(
            (
                float(score),
                {
                    "title": next(
                        (
                            line.removeprefix("# ").strip()
                            for line in text.splitlines()
                            if line.startswith("# ")
                        ),
                        path.stem,
                    ),
                    "summary_relative_path": relative_path,
                    "source_relative_path": metadata["source_path"],
                    "source_name": metadata.get("source_name"),
                    "total_pages": metadata.get("total_pages"),
                    "score": float(score),
                    "summary": text[:12_000],
                },
            )
        )
    scored.sort(key=lambda item: item[0], reverse=True)
    matches = [match for _, match in scored[:top_k]]
    return {"status": "searched", "query": query, "matches": matches, "count": len(matches)}
