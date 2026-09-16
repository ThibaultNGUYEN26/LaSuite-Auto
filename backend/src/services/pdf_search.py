"""Bounded, page-aware retrieval across a collection of PDF documents."""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter, OrderedDict
from dataclasses import dataclass
from threading import RLock
from typing import Callable, Iterable

from agent.errors import AgentError, SpecialistAgentError
from services.pdf import extract_pdf_pages

CHUNK_CHARACTERS = 2_400
CHUNK_OVERLAP = 240
TOKEN_PATTERN = re.compile(r"[^\W_]{2,}", re.UNICODE)
STOP_WORDS = {
    "about", "avec", "avoir", "cette", "dans", "des", "does", "est", "for",
    "from", "have", "how", "les", "mais", "mon", "pour", "quel", "quelle",
    "should", "that", "the", "this", "une", "what", "when", "where", "which",
    "with", "your",
}


@dataclass(frozen=True)
class PdfSource:
    """One lazily loaded PDF in a source block."""

    cache_key: str
    name: str
    reference: str
    load: Callable[[], bytes]


@dataclass(frozen=True)
class _Chunk:
    source_name: str
    source_reference: str
    page: int
    text: str
    tokens: tuple[str, ...]


class PdfPageCache:
    """Small process-local LRU cache that avoids reparsing PDFs every turn."""

    def __init__(self, *, max_documents: int = 64, max_characters: int = 8_000_000):
        self.max_documents = max_documents
        self.max_characters = max_characters
        self._items: OrderedDict[str, tuple[list[str], int]] = OrderedDict()
        self._characters = 0
        self._lock = RLock()

    def get(self, key: str) -> list[str] | None:
        with self._lock:
            stored = self._items.get(key)
            if stored is None:
                return None
            self._items.move_to_end(key)
            return stored[0]

    def put(self, key: str, pages: list[str]) -> None:
        size = sum(len(page) for page in pages)
        if size > self.max_characters:
            return
        with self._lock:
            previous = self._items.pop(key, None)
            if previous is not None:
                self._characters -= previous[1]
            self._items[key] = (pages, size)
            self._characters += size
            while (
                len(self._items) > self.max_documents
                or self._characters > self.max_characters
            ):
                _, (_, removed_size) = self._items.popitem(last=False)
                self._characters -= removed_size

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
            self._characters = 0


pdf_page_cache = PdfPageCache()


def search_tokens(value: str) -> tuple[str, ...]:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    return tuple(
        token
        for token in TOKEN_PATTERN.findall(normalized)
        if token not in STOP_WORDS
    )


def _page_chunks(text: str) -> Iterable[str]:
    clean = re.sub(r"[ \t]+", " ", text).strip()
    if len(clean) <= CHUNK_CHARACTERS:
        if clean:
            yield clean
        return
    start = 0
    while start < len(clean):
        end = min(start + CHUNK_CHARACTERS, len(clean))
        if end < len(clean):
            boundary = max(clean.rfind("\n", start, end), clean.rfind(". ", start, end))
            if boundary > start + CHUNK_CHARACTERS // 2:
                end = boundary + 1
        chunk = clean[start:end].strip()
        if chunk:
            yield chunk
        if end >= len(clean):
            break
        start = max(end - CHUNK_OVERLAP, start + 1)


def _rank_chunks(query: str, chunks: list[_Chunk], *, top_k: int) -> list[dict]:
    query_tokens = search_tokens(query)
    if not query_tokens:
        raise SpecialistAgentError("The PDF search question is too short")
    if not chunks:
        return []

    document_frequency: Counter[str] = Counter()
    for chunk in chunks:
        document_frequency.update(set(chunk.tokens))

    total_chunks = len(chunks)
    average_length = sum(len(chunk.tokens) for chunk in chunks) / total_chunks
    query_counts = Counter(query_tokens)
    scored: list[tuple[float, _Chunk]] = []
    for chunk in chunks:
        frequencies = Counter(chunk.tokens)
        score = 0.0
        for token, query_frequency in query_counts.items():
            frequency = frequencies.get(token, 0)
            if not frequency:
                continue
            frequency_in_docs = document_frequency[token]
            inverse_frequency = math.log(
                1 + (total_chunks - frequency_in_docs + 0.5) / (frequency_in_docs + 0.5)
            )
            length_normalization = frequency + 1.5 * (
                0.25 + 0.75 * len(chunk.tokens) / max(average_length, 1)
            )
            score += (
                inverse_frequency
                * frequency
                * 2.5
                / length_normalization
                * min(query_frequency, 2)
            )

        filename_tokens = set(search_tokens(chunk.source_name))
        score += 0.35 * len(filename_tokens.intersection(query_counts))
        # Tables of contents are useful navigation hints but are weak evidence for
        # an answer. Dot-leader-heavy chunks should rank below the actual page text.
        if len(re.findall(r"\.{5,}\s*\d+", chunk.text)) >= 3:
            score *= 0.3
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    matches: list[dict] = []
    seen: set[tuple[str, int, str]] = set()
    for score, chunk in scored:
        fingerprint = (chunk.source_reference, chunk.page, chunk.text[:120])
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        matches.append(
            {
                "source_name": chunk.source_name,
                "source_reference": chunk.source_reference,
                "page": chunk.page,
                "score": round(score, 4),
                "excerpt": chunk.text,
                "citation": f"[{chunk.source_name}, p. {chunk.page}]",
            }
        )
        if len(matches) >= top_k:
            break
    return matches


def search_pdf_sources(
    sources: Iterable[PdfSource],
    *,
    query: str,
    top_k: int = 8,
    max_total_pages: int = 2_000,
) -> dict:
    """Extract, cache, and rank relevant page chunks from multiple PDFs."""
    if not query.strip():
        raise SpecialistAgentError("query must be a non-empty string")
    if not 1 <= top_k <= 20:
        raise SpecialistAgentError("top_k must be between 1 and 20")
    if max_total_pages < 1:
        raise SpecialistAgentError("max_total_pages must be positive")

    chunks: list[_Chunk] = []
    scanned_documents = 0
    scanned_pages = 0
    skipped: list[dict[str, str]] = []
    corpus_limited = False

    for source in sources:
        if scanned_pages >= max_total_pages:
            corpus_limited = True
            break
        pages = pdf_page_cache.get(source.cache_key)
        if pages is None:
            try:
                pages = extract_pdf_pages(source.load())
            except (AgentError, OSError) as exc:
                skipped.append({"source_name": source.name, "reason": str(exc)})
                continue
            pdf_page_cache.put(source.cache_key, pages)

        scanned_documents += 1
        remaining_pages = max_total_pages - scanned_pages
        selected_pages = pages[:remaining_pages]
        if len(selected_pages) < len(pages):
            corpus_limited = True
        scanned_pages += len(selected_pages)
        for page_number, page_text in enumerate(selected_pages, start=1):
            for text in _page_chunks(page_text):
                tokens = search_tokens(text)
                if tokens:
                    chunks.append(
                        _Chunk(
                            source_name=source.name,
                            source_reference=source.reference,
                            page=page_number,
                            text=text,
                            tokens=tokens,
                        )
                    )

    matches = _rank_chunks(query, chunks, top_k=top_k)
    return {
        "status": "searched",
        "query": query,
        "documents_scanned": scanned_documents,
        "pages_scanned": scanned_pages,
        "matches": matches,
        "match_count": len(matches),
        "skipped_documents": skipped,
        "corpus_limited": corpus_limited,
        "grounding_instruction": (
            "Answer only from these excerpts. Cite each factual claim with the "
            "provided [filename, p. N] citation. If they do not answer the question, "
            "say that no supporting passage was found."
        ),
    }
