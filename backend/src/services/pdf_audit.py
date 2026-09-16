"""Evidence-grounded audit of one client PDF against one reference PDF."""

from __future__ import annotations

import asyncio
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agent.artifacts import Artifact
from agent.errors import LocalFilesError, PdfError
from services.local_files import (
    list_local_items,
    read_local_pdf,
    read_local_text,
    resolve_local_file,
)
from services.pdf import extract_pdf_pages
from services.pdf_memory import SummaryChatClient, complete_text, load_pdf_memory
from services.pdf_search import PdfSource, search_pdf_sources, search_tokens

TEXT_EVIDENCE_EXTENSIONS = {
    ".csv", ".tsv", ".txt", ".md", ".json", ".yaml", ".yml", ".log"
}
AUDIT_BATCH_SIZE = 5
AUDIT_BATCH_CONCURRENCY = 2
CRITERIA_INPUT_CHARACTERS = 40_000
MAX_AUDIT_CRITERIA = 100

CRITERIA_PROMPT = (
    "Extract every distinct audit criterion from this original reference-document "
    "excerpt. "
    "Return only JSON in this form: "
    '{"criteria":[{"name":"...","requirement":"...","query":"..."}]}. '
    "Create distinct, auditable criteria rather than broad themes. Preserve every "
    "material requirement, proof requirement, exception, and sign-off requirement. "
    "The query must contain reference vocabulary and synonyms suitable for retrieving "
    "evidence from both the reference and client documents. Do not merge separate "
    "requirements merely to shorten the response."
)

AUDIT_PROMPT = (
    "Audit one client document against one reference document using only the original-"
    "page evidence supplied below. For every criterion, report exactly one status: "
    "COMPLIANT, NON-COMPLIANT, or INSUFFICIENT EVIDENCE. COMPLIANT requires affirmative "
    "client evidence satisfying the reference. NON-COMPLIANT requires explicit client "
    "evidence of a failure or contradiction. Missing, vague, placeholder, or unsupported "
    "claims are INSUFFICIENT EVIDENCE, not compliant and not automatically non-compliant. "
    "For each criterion include: requirement, verdict, reference evidence, client "
    "evidence, reasoning, and corrective action. Cite every factual statement exactly "
    "as [filename, p. N]. Never use outside knowledge, invent evidence, or treat the "
    "memory as evidence. Finish with an overall result and evidence limitations."
)

CORPUS_AUDIT_PROMPT = (
    "Assess every supplied criterion against the complete client evidence corpus. "
    "Return only JSON as {\"findings\":[...]}. Return exactly one finding for each "
    "criterion_number supplied, without grouping or omission. Each finding must have "
    "criterion_number (integer), status (COMPLIANT, NON-COMPLIANT, or INSUFFICIENT "
    "EVIDENCE), requirement, reference_evidence, client_evidence, reasoning, and "
    "corrective_action (all strings). COMPLIANT requires affirmative client evidence. "
    "NON-COMPLIANT requires explicit evidence of failure or contradiction. Missing, "
    "vague, placeholder, or unsupported claims are INSUFFICIENT EVIDENCE. Use only the "
    "supplied original-page or original-line excerpts and preserve their exact "
    "citations. Never use outside knowledge or treat filenames as evidence."
)


@dataclass(frozen=True)
class _TextChunk:
    source: str
    start_line: int
    end_line: int
    text: str
    tokens: tuple[str, ...]


def _parse_criteria(raw: str) -> list[dict[str, str]]:
    start, end = raw.find("{"), raw.rfind("}")
    try:
        payload = json.loads(raw[start : end + 1])
    except (json.JSONDecodeError, TypeError):
        payload = {}
    values = payload.get("criteria") if isinstance(payload, dict) else None
    criteria: list[dict[str, str]] = []
    if isinstance(values, list):
        if len(values) > MAX_AUDIT_CRITERIA:
            raise PdfError(
                f"The reference produced more than {MAX_AUDIT_CRITERIA} audit criteria"
            )
        for value in values:
            if not isinstance(value, dict):
                continue
            name = value.get("name")
            requirement = value.get("requirement")
            query = value.get("query")
            if all(isinstance(item, str) and item.strip() for item in (name, requirement, query)):
                criteria.append(
                    {
                        "name": name.strip(),
                        "requirement": requirement.strip(),
                        "query": query.strip(),
                    }
                )
    if not criteria:
        raise PdfError("Could not extract audit criteria from the reference PDF")
    return criteria


def _reference_criteria_batches(pages: list[str]) -> list[str]:
    batches: list[str] = []
    current: list[str] = []
    size = 0
    for page_number, page in enumerate(pages, start=1):
        offset = 0
        while offset < len(page):
            segment = page[offset : offset + CRITERIA_INPUT_CHARACTERS - 64]
            labelled = f"[Page {page_number}]\n{segment}"
            if current and size + len(labelled) + 2 > CRITERIA_INPUT_CHARACTERS:
                batches.append("\n\n".join(current))
                current = []
                size = 0
            current.append(labelled)
            size += len(labelled) + 2
            offset += len(segment)
    if current:
        batches.append("\n\n".join(current))
    return batches


async def _extract_reference_criteria(
    root: Path,
    *,
    audit_relative_path: str,
    focus: str | None,
    client: SummaryChatClient,
    model: str,
    max_read_bytes: int,
) -> tuple[list[dict[str, str]], int]:
    pages = extract_pdf_pages(
        read_local_pdf(root, audit_relative_path, max_bytes=max_read_bytes)
    )
    batches = _reference_criteria_batches(pages)
    if not batches:
        raise PdfError("No extractable audit criteria were found in the reference PDF")

    raw_results = await asyncio.gather(
        *(
            complete_text(
                client,
                model=model,
                system=CRITERIA_PROMPT,
                content=(
                    f"Requested audit focus: {focus or 'Complete audit'}\n"
                    f"Reference excerpt {index} of {len(batches)}:\n\n{batch}"
                ),
            )
            for index, batch in enumerate(batches, start=1)
        )
    )
    criteria: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for raw in raw_results:
        for criterion in _parse_criteria(raw):
            fingerprint = (
                " ".join(criterion["name"].casefold().split()),
                " ".join(criterion["requirement"].casefold().split()),
            )
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            criteria.append(criterion)
    if len(criteria) > MAX_AUDIT_CRITERIA:
        raise PdfError(
            f"The reference contains more than {MAX_AUDIT_CRITERIA} audit criteria; "
            "narrow the requested audit focus"
        )
    return criteria, len(raw_results)


def _pdf_source(
    root: Path,
    relative_path: str,
    *,
    max_read_bytes: int,
    display_name: str | None = None,
) -> PdfSource:
    source = resolve_local_file(root, relative_path)
    if source.suffix.lower() != ".pdf":
        raise PdfError("Auditing requires PDF files")
    stat = source.stat()
    return PdfSource(
        cache_key=f"local:{relative_path}:{stat.st_mtime_ns}:{stat.st_size}",
        name=display_name or source.name,
        reference=relative_path,
        load=lambda: read_local_pdf(root, relative_path, max_bytes=max_read_bytes),
    )


def _source_entry(
    *, source_id: str, role: str, relative_path: str, media_type: str
) -> dict[str, Any]:
    is_pdf = media_type == "application/pdf"
    retrieval = (
        "Open this file and go to the cited page."
        if is_pdf
        else "Open this file and go to the cited line range."
    )
    return {
        "source_id": source_id,
        "role": role,
        "name": Path(relative_path).name,
        "type": "PDF" if is_pdf else Path(relative_path).suffix.lstrip(".").upper(),
        "relative_path": relative_path,
        "retrieval": retrieval,
        "retrieval_prompt": (
            f"Open `{relative_path}` and show the evidence at the page or line "
            "range cited in the audit."
        ),
        "artifact": Artifact(
            kind="file",
            location="local",
            reference=relative_path,
            media_type=media_type,
            name=Path(relative_path).name,
            metadata={"source_id": source_id, "role": role},
        ).tool_value(),
    }


def _source_register_markdown(source_register: list[dict[str, Any]]) -> str:
    def table_cell(value: str) -> str:
        return " ".join(value.split()).replace("|", "\\|")

    lines = [
        "## Source register",
        "",
        "Ask Auto to reopen a source by its source ID or exact location. PDF "
        "citations point to a page; CSV/text citations point to a line range.",
        "",
        "| Source ID | Role | Document | Type | Exact location | Retrieval |",
        "|---|---|---|---|---|---|",
    ]
    for source in source_register:
        cells = [
            source["source_id"],
            source["role"],
            source["name"],
            source["type"],
            f"`{source['relative_path']}`",
            source["retrieval"],
        ]
        lines.append("| " + " | ".join(table_cell(cell) for cell in cells) + " |")
    return "\n".join(lines)


async def audit_pdf_against_reference(
    root: Path,
    *,
    audit_relative_path: str,
    client_relative_path: str,
    focus: str | None,
    client: SummaryChatClient,
    model: str,
    max_read_bytes: int,
    max_total_pages: int,
) -> dict[str, Any]:
    """Build a complete checklist, retrieve both sides, and render verdicts."""
    if audit_relative_path == client_relative_path:
        raise PdfError("The audit reference and client document must be different")
    reference_memory = load_pdf_memory(
        root, source_relative_path=audit_relative_path
    )
    client_memory = load_pdf_memory(root, source_relative_path=client_relative_path)
    if reference_memory is None or not reference_memory["up_to_date"]:
        raise PdfError("The audit reference must be prepared before auditing")
    if client_memory is None or not client_memory["up_to_date"]:
        raise PdfError("The client document must be prepared before auditing")

    criteria, _ = await _extract_reference_criteria(
        root,
        audit_relative_path=audit_relative_path,
        focus=focus,
        client=client,
        model=model,
        max_read_bytes=max_read_bytes,
    )
    reference_source = _pdf_source(
        root, audit_relative_path, max_read_bytes=max_read_bytes
    )
    client_source = _pdf_source(
        root, client_relative_path, max_read_bytes=max_read_bytes
    )

    evidence_sections: list[str] = []
    for index, criterion in enumerate(criteria, start=1):
        section = [
            f"## Criterion {index}: {criterion['name']}",
            f"Requirement: {criterion['requirement']}",
            f"Retrieval query: {criterion['query']}",
        ]
        for label, source, top_k in (
            ("REFERENCE", reference_source, 1),
            ("CLIENT", client_source, 2),
        ):
            result = search_pdf_sources(
                [source],
                query=criterion["query"],
                top_k=top_k,
                max_total_pages=max_total_pages,
            )
            section.append(f"### {label}: {source.name}")
            if not result["matches"]:
                section.append("No supporting passage found.")
            else:
                section.extend(
                    f"{match['citation']}\n{match['excerpt']}"
                    for match in result["matches"]
                )
        evidence_sections.append("\n\n".join(section))

    audit = await complete_text(
        client,
        model=model,
        system=AUDIT_PROMPT,
        content=(
            f"Requested focus: {focus or 'Complete audit'}\n"
            f"Reference document: {reference_source.name}\n"
            f"Client document: {client_source.name}\n\n"
            + "\n\n---\n\n".join(evidence_sections)
        ),
    )
    source_register = [
        _source_entry(
            source_id="REF",
            role="Audit reference",
            relative_path=audit_relative_path,
            media_type="application/pdf",
        ),
        _source_entry(
            source_id="SRC-001",
            role="Client evidence",
            relative_path=client_relative_path,
            media_type="application/pdf",
        ),
    ]
    audit = f"{_source_register_markdown(source_register)}\n\n{audit.strip()}"
    return {
        "status": "audited",
        "audit_reference": audit_relative_path,
        "client_document": client_relative_path,
        "criteria_count": len(criteria),
        "source_register_count": len(source_register),
        "sources": source_register,
        "audit": audit,
        "grounded": True,
    }


def _text_chunks(
    relative_path: str,
    content: str,
    *,
    lines_per_chunk: int = 30,
    overlap: int = 5,
) -> list[_TextChunk]:
    """Split text evidence while retaining stable, user-verifiable line citations."""
    lines = content.splitlines()
    chunks: list[_TextChunk] = []
    start = 0
    while start < len(lines):
        end = min(start + lines_per_chunk, len(lines))
        text = "\n".join(lines[start:end]).strip()
        tokens = search_tokens(text)
        if text and tokens:
            chunks.append(
                _TextChunk(
                    source=relative_path,
                    start_line=start + 1,
                    end_line=end,
                    text=text,
                    tokens=tokens,
                )
            )
        if end >= len(lines):
            break
        start = max(end - overlap, start + 1)
    return chunks


def _search_text_chunks(
    chunks: list[_TextChunk], query: str, *, top_k: int = 2
) -> list[dict[str, Any]]:
    query_counts = Counter(search_tokens(query))
    if not query_counts:
        return []
    scored: list[tuple[float, _TextChunk]] = []
    for chunk in chunks:
        frequencies = Counter(chunk.tokens)
        score = sum(
            min(frequencies.get(token, 0), 3) * min(query_count, 2)
            for token, query_count in query_counts.items()
        )
        score += 0.5 * len(
            set(search_tokens(chunk.source)).intersection(query_counts)
        )
        if score:
            scored.append((float(score), chunk))
    scored.sort(key=lambda value: value[0], reverse=True)
    return [
        {
            "citation": (
                f"[{chunk.source}, lines {chunk.start_line}-{chunk.end_line}]"
            ),
            "excerpt": chunk.text,
            "score": score,
        }
        for score, chunk in scored[:top_k]
    ]


def _parse_findings(
    raw: str, criteria_by_number: dict[int, dict[str, str]]
) -> dict[int, dict[str, str]]:
    start, end = raw.find("{"), raw.rfind("}")
    try:
        payload = json.loads(raw[start : end + 1])
    except (json.JSONDecodeError, TypeError):
        return {}
    values = payload.get("findings") if isinstance(payload, dict) else None
    if not isinstance(values, list):
        return {}
    valid_statuses = {"COMPLIANT", "NON-COMPLIANT", "INSUFFICIENT EVIDENCE"}
    findings: dict[int, dict[str, str]] = {}
    for value in values:
        if not isinstance(value, dict):
            continue
        number = value.get("criterion_number")
        if not isinstance(number, int) or number not in criteria_by_number:
            continue
        status = str(value.get("status", "")).strip().upper().replace("_", " ")
        if status not in valid_statuses:
            continue
        criterion = criteria_by_number[number]
        findings[number] = {
            "name": criterion["name"],
            "requirement": str(value.get("requirement") or criterion["requirement"]).strip(),
            "status": status,
            "reference_evidence": str(value.get("reference_evidence") or "No supporting passage found.").strip(),
            "client_evidence": str(value.get("client_evidence") or "No supporting passage found.").strip(),
            "reasoning": str(value.get("reasoning") or "The supplied evidence does not establish the requirement.").strip(),
            "corrective_action": str(value.get("corrective_action") or "Provide evidence that directly addresses this requirement.").strip(),
        }
    return findings


def _render_corpus_audit(
    *,
    client_directory: str,
    criteria: list[dict[str, str]],
    findings: dict[int, dict[str, str]],
    pdf_paths: list[str],
    text_paths: list[str],
    source_register: list[dict[str, Any]],
    limitations: list[str],
) -> tuple[str, str]:
    def table_cell(value: str) -> str:
        return " ".join(value.split()).replace("|", "\\|")

    counts = Counter(finding["status"] for finding in findings.values())
    if counts["NON-COMPLIANT"]:
        overall = "NON-COMPLIANT"
    elif counts["INSUFFICIENT EVIDENCE"]:
        overall = "INCOMPLETE — INSUFFICIENT EVIDENCE"
    else:
        overall = "COMPLIANT"

    lines = [
        f"# Audit report — {client_directory}",
        "",
        "## Overall result",
        "",
        f"**{overall}**",
        "",
        f"- Compliant: {counts['COMPLIANT']}",
        f"- Non-compliant: {counts['NON-COMPLIANT']}",
        f"- Insufficient evidence: {counts['INSUFFICIENT EVIDENCE']}",
        f"- Criteria assessed: {len(criteria)}",
        "",
        "## Source register",
        "",
        f"Assessed {len(pdf_paths)} PDF file(s) and {len(text_paths)} text/tabular file(s).",
        "",
        "Use the exact location with Auto to reopen a source. PDF citations point "
        "to a page; CSV/text citations point to a line range. The source IDs and "
        "file artifacts below are also returned as structured audit data so a "
        "later request can retrieve the evidence without rediscovering it.",
        "",
        "| Source ID | Role | Document | Type | Exact location | Retrieval |",
        "|---|---|---|---|---|---|",
    ]
    for source in source_register:
        cells = [
            source["source_id"],
            source["role"],
            source["name"],
            source["type"],
            f"`{source['relative_path']}`",
            source["retrieval"],
        ]
        lines.append("| " + " | ".join(table_cell(cell) for cell in cells) + " |")

    lines.extend(
        [
            "",
            "## Complete audit matrix",
            "",
            "| # | Criterion | Requirement | Verdict | Reference evidence | Client evidence | Reasoning | Corrective action |",
            "|---:|---|---|---|---|---|---|---|",
        ]
    )
    for number, criterion in enumerate(criteria, start=1):
        finding = findings[number]
        cells = [
            str(number),
            criterion["name"],
            finding["requirement"],
            finding["status"],
            finding["reference_evidence"],
            finding["client_evidence"],
            finding["reasoning"],
            finding["corrective_action"],
        ]
        lines.append("| " + " | ".join(table_cell(cell) for cell in cells) + " |")
    lines.extend(["", "## Detailed findings", ""])
    for number, criterion in enumerate(criteria, start=1):
        finding = findings[number]
        lines.extend(
            [
                f"### {number}. {criterion['name']}",
                "",
                f"- **Verdict:** {finding['status']}",
                f"- **Requirement:** {finding['requirement']}",
                f"- **Reference evidence:** {finding['reference_evidence']}",
                f"- **Client evidence:** {finding['client_evidence']}",
                f"- **Reasoning:** {finding['reasoning']}",
                f"- **Corrective action:** {finding['corrective_action']}",
                "",
            ]
        )
    if limitations:
        lines.extend(["## Limitations", ""])
        lines.extend(f"- {limitation}" for limitation in limitations)
    else:
        lines.extend(
            [
                "## Limitations",
                "",
                "No technical corpus limitation was detected for the selected folder.",
            ]
        )
    return "\n".join(lines).strip(), overall


async def audit_folder_against_reference(
    root: Path,
    *,
    audit_relative_path: str,
    client_directory: str,
    focus: str | None,
    client: SummaryChatClient,
    model: str,
    max_read_bytes: int,
    max_text_characters: int,
    max_files: int,
    max_total_pages: int,
    recursive: bool = True,
    max_depth: int = 5,
) -> dict[str, Any]:
    """Audit a complete client folder in one bounded, completeness-checked run."""
    reference_memory = load_pdf_memory(root, source_relative_path=audit_relative_path)
    if reference_memory is None or not reference_memory["up_to_date"]:
        raise PdfError("The audit reference must be prepared before auditing")

    listing = list_local_items(
        root,
        directory=client_directory,
        limit=500,
        recursive=recursive,
        max_depth=max_depth,
    )
    supported = [
        item
        for item in listing["items"]
        if item["type"] == "file"
        and item["relative_path"] != audit_relative_path
        and (item["extension"] == ".pdf" or item["extension"] in TEXT_EVIDENCE_EXTENSIONS)
    ]
    if not supported:
        raise PdfError("The selected client folder contains no supported evidence files")

    limitations: list[str] = []
    if not listing["complete"] and listing.get("limitation"):
        limitations.append(str(listing["limitation"]))
    if len(supported) > max_files:
        limitations.append(
            f"Only the first {max_files} supported evidence files were assessed."
        )
        supported = supported[:max_files]

    pdf_paths = [item["relative_path"] for item in supported if item["extension"] == ".pdf"]
    text_paths = [item["relative_path"] for item in supported if item["extension"] != ".pdf"]
    reference_source = _pdf_source(
        root,
        audit_relative_path,
        max_read_bytes=max_read_bytes,
        display_name=audit_relative_path,
    )
    pdf_sources = [
        _pdf_source(
            root,
            path,
            max_read_bytes=max_read_bytes,
            display_name=path,
        )
        for path in pdf_paths
    ]

    text_chunks: list[_TextChunk] = []
    readable_text_paths: list[str] = []
    for path in text_paths:
        try:
            result = read_local_text(
                root,
                path,
                max_bytes=max_read_bytes,
                max_characters=max_text_characters,
            )
        except (LocalFilesError, OSError) as exc:
            limitations.append(f"Could not read `{path}`: {exc}")
            continue
        readable_text_paths.append(path)
        text_chunks.extend(_text_chunks(path, result["content"]))
        if result["truncated"]:
            limitations.append(f"Only part of `{path}` could be read.")

    source_register = [
        _source_entry(
            source_id="REF",
            role="Audit reference",
            relative_path=audit_relative_path,
            media_type="application/pdf",
        )
    ]
    for index, path in enumerate([*pdf_paths, *readable_text_paths], start=1):
        suffix = Path(path).suffix.lower()
        media_type = {
            ".pdf": "application/pdf",
            ".csv": "text/csv",
            ".json": "application/json",
            ".md": "text/markdown",
        }.get(suffix, "text/plain")
        source_register.append(
            _source_entry(
                source_id=f"SRC-{index:03d}",
                role="Client evidence",
                relative_path=path,
                media_type=media_type,
            )
        )

    criteria, criteria_calls = await _extract_reference_criteria(
        root,
        audit_relative_path=audit_relative_path,
        focus=focus,
        client=client,
        model=model,
        max_read_bytes=max_read_bytes,
    )

    evidence_by_number: dict[int, str] = {}
    for number, criterion in enumerate(criteria, start=1):
        reference_result = search_pdf_sources(
            [reference_source],
            query=criterion["query"],
            top_k=1,
            max_total_pages=max_total_pages,
        )
        client_result = search_pdf_sources(
            pdf_sources,
            query=criterion["query"],
            top_k=5,
            max_total_pages=max_total_pages,
        ) if pdf_sources else {"matches": [], "skipped_documents": [], "corpus_limited": False}
        if client_result.get("corpus_limited"):
            limitation = "The configured PDF page budget did not cover every client page."
            if limitation not in limitations:
                limitations.append(limitation)
        for skipped in client_result.get("skipped_documents", []):
            limitation = f"Could not read `{skipped['source_name']}`: {skipped['reason']}"
            if limitation not in limitations:
                limitations.append(limitation)

        reference_matches = reference_result["matches"]
        client_matches = client_result["matches"]
        tabular_matches = _search_text_chunks(text_chunks, criterion["query"], top_k=3)
        sections = [
            f"CRITERION {number}: {criterion['name']}",
            f"Requirement: {criterion['requirement']}",
            "REFERENCE EVIDENCE:",
            *(
                [f"{match['citation']}\n{match['excerpt'][:1600]}" for match in reference_matches]
                or ["No supporting passage found."]
            ),
            "CLIENT PDF EVIDENCE:",
            *(
                [f"{match['citation']}\n{match['excerpt'][:1600]}" for match in client_matches]
                or ["No supporting passage found."]
            ),
            "CLIENT TEXT/TABULAR EVIDENCE:",
            *(
                [f"{match['citation']}\n{match['excerpt'][:1600]}" for match in tabular_matches]
                or ["No supporting passage found."]
            ),
        ]
        evidence_by_number[number] = "\n\n".join(sections)

    semaphore = asyncio.Semaphore(AUDIT_BATCH_CONCURRENCY)

    async def assess_batch(numbers: list[int]) -> tuple[dict[int, dict[str, str]], int]:
        criteria_map = {number: criteria[number - 1] for number in numbers}
        content = (
            f"Requested focus: {focus or 'Complete audit'}\n"
            f"Client folder: {client_directory}\n\n"
            + "\n\n---\n\n".join(evidence_by_number[number] for number in numbers)
        )
        calls = 0
        async with semaphore:
            raw = await complete_text(
                client, model=model, system=CORPUS_AUDIT_PROMPT, content=content
            )
            calls += 1
            findings = _parse_findings(raw, criteria_map)
            if set(findings) != set(numbers):
                raw = await complete_text(
                    client,
                    model=model,
                    system=CORPUS_AUDIT_PROMPT,
                    content=(
                        "Your previous response was incomplete or invalid. Return every "
                        "requested criterion exactly once.\n\n" + content
                    ),
                )
                calls += 1
                findings = _parse_findings(raw, criteria_map)
        return findings, calls

    batches = [
        list(range(start, min(start + AUDIT_BATCH_SIZE, len(criteria) + 1)))
        for start in range(1, len(criteria) + 1, AUDIT_BATCH_SIZE)
    ]
    batch_results = await asyncio.gather(*(assess_batch(batch) for batch in batches))
    findings: dict[int, dict[str, str]] = {}
    model_calls = criteria_calls
    for batch_findings, calls in batch_results:
        findings.update(batch_findings)
        model_calls += calls

    missing = []
    for number, criterion in enumerate(criteria, start=1):
        if number in findings:
            continue
        missing.append(number)
        findings[number] = {
            "name": criterion["name"],
            "requirement": criterion["requirement"],
            "status": "INSUFFICIENT EVIDENCE",
            "reference_evidence": "The model did not return a usable finding.",
            "client_evidence": "The model did not return a usable finding.",
            "reasoning": "This criterion could not be evaluated reliably in this run.",
            "corrective_action": "Retry this criterion before relying on the audit.",
        }
    if missing:
        limitations.append(
            "Some criteria could not be evaluated reliably: "
            + ", ".join(str(number) for number in missing)
            + "."
        )

    report, overall = _render_corpus_audit(
        client_directory=client_directory,
        criteria=criteria,
        findings=findings,
        pdf_paths=pdf_paths,
        text_paths=readable_text_paths,
        source_register=source_register,
        limitations=limitations,
    )
    return {
        "status": "audited",
        "overall_result": overall,
        "audit_reference": audit_relative_path,
        "client_directory": client_directory,
        "criteria_count": len(criteria),
        "source_count": len(pdf_paths) + len(readable_text_paths),
        "source_register_count": len(source_register),
        "pdf_count": len(pdf_paths),
        "text_count": len(readable_text_paths),
        "sources": source_register,
        "criteria": criteria,
        "findings": [
            {"criterion_number": number, **findings[number]}
            for number in range(1, len(criteria) + 1)
        ],
        "audit": report,
        "grounded": True,
        "complete": not limitations,
        "limitations": limitations,
        "model_calls": model_calls,
    }
