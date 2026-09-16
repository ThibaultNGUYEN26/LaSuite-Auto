"""Evidence-grounded comparison of two remembered local PDFs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent.errors import PdfError
from services.local_files import read_local_pdf, resolve_local_file
from services.pdf_memory import SummaryChatClient, complete_text, load_pdf_memory
from services.pdf_search import PdfSource, search_pdf_sources

PLAN_PROMPT = (
    "Plan a useful comparison of exactly two PDF documents from their memory guides. "
    "Return only JSON: {\"dimensions\":[{\"name\":\"...\",\"query\":\"...\"}]}. "
    "Choose 3 to 6 concrete dimensions that expose similarities, differences, "
    "contradictions, requirements, recommendations, scope, or omissions. Each query "
    "must contain document vocabulary and synonyms suitable for passage retrieval."
)

COMPARE_PROMPT = (
    "Compare two PDFs using only the retrieved page evidence below. Return Markdown "
    "with: Executive comparison, Side-by-side table, Agreements, Differences, "
    "Contradictions, Unique coverage, and Evidence limitations. Every factual claim "
    "must cite [filename, p. N]. Distinguish a true contradiction from information "
    "that is merely absent in one document. Never use outside knowledge or memory-guide "
    "claims that are not supported by the retrieved original-page excerpts."
)


def _parse_dimensions(raw: str, *, focus: str | None) -> list[dict[str, str]]:
    start, end = raw.find("{"), raw.rfind("}")
    try:
        payload = json.loads(raw[start : end + 1])
    except (json.JSONDecodeError, TypeError):
        payload = {}
    values = payload.get("dimensions") if isinstance(payload, dict) else None
    dimensions: list[dict[str, str]] = []
    if isinstance(values, list):
        for value in values[:6]:
            if not isinstance(value, dict):
                continue
            name, query = value.get("name"), value.get("query")
            if isinstance(name, str) and name.strip() and isinstance(query, str) and query.strip():
                dimensions.append({"name": name.strip(), "query": query.strip()})
    if dimensions:
        return dimensions
    fallback = focus.strip() if isinstance(focus, str) and focus.strip() else (
        "purpose scope requirements recommendations differences"
    )
    return [{"name": "Requested comparison", "query": fallback}]


async def compare_pdf_memories(
    root: Path,
    *,
    relative_paths: list[str],
    focus: str | None,
    client: SummaryChatClient,
    model: str,
    max_read_bytes: int,
    max_total_pages: int,
) -> dict[str, Any]:
    if len(relative_paths) != 2 or relative_paths[0] == relative_paths[1]:
        raise PdfError("Comparison requires two different PDF paths")

    memories = []
    sources = []
    for relative_path in relative_paths:
        source = resolve_local_file(root, relative_path)
        if source.suffix.lower() != ".pdf":
            raise PdfError("Comparison requires PDF files")
        memory = load_pdf_memory(root, source_relative_path=relative_path)
        if memory is None or not memory["up_to_date"]:
            raise PdfError(
                f"Create or refresh the PDF memory for {relative_path} before comparing"
            )
        memories.append(memory)
        stat = source.stat()
        sources.append(
            PdfSource(
                cache_key=f"local:{relative_path}:{stat.st_mtime_ns}:{stat.st_size}",
                name=source.name,
                reference=relative_path,
                load=lambda path=relative_path: read_local_pdf(
                    root, path, max_bytes=max_read_bytes
                ),
            )
        )

    plan_input = (
        f"Requested focus: {focus or 'Comprehensive comparison'}\n\n"
        f"DOCUMENT A MEMORY\n{memories[0]['content'][:24_000]}\n\n"
        f"DOCUMENT B MEMORY\n{memories[1]['content'][:24_000]}"
    )
    plan = await complete_text(
        client,
        model=model,
        system=PLAN_PROMPT,
        content=plan_input,
    )
    dimensions = _parse_dimensions(plan, focus=focus)

    evidence_sections: list[str] = []
    for dimension in dimensions:
        section = [f"## {dimension['name']}", f"Retrieval query: {dimension['query']}"]
        for source in sources:
            result = search_pdf_sources(
                [source],
                query=dimension["query"],
                top_k=2,
                max_total_pages=max_total_pages,
            )
            section.append(f"### {source.name}")
            if not result["matches"]:
                section.append("No supporting passage found.")
            else:
                for match in result["matches"]:
                    section.append(f"{match['citation']}\n{match['excerpt']}")
        evidence_sections.append("\n\n".join(section))

    comparison = await complete_text(
        client,
        model=model,
        system=COMPARE_PROMPT,
        content=(
            f"User focus: {focus or 'Comprehensive comparison'}\n\n"
            + "\n\n---\n\n".join(evidence_sections)
        ),
    )
    return {
        "status": "compared",
        "sources": relative_paths,
        "dimensions": dimensions,
        "comparison": comparison,
        "grounded": True,
    }
