"""Shared bounded decoding for text-based file specialists."""

from __future__ import annotations

from pathlib import Path

from agent.errors import SpecialistAgentError


READABLE_TEXT_EXTENSIONS = {
    ".csv",
    ".json",
    ".log",
    ".md",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


def decode_text_content(
    data: bytes,
    *,
    filename: str,
    max_characters: int,
    error_type: type[SpecialistAgentError],
) -> tuple[str, str, int, bool]:
    """Validate a text extension and decode bytes without leaking unbounded text."""
    if Path(filename).suffix.lower() not in READABLE_TEXT_EXTENSIONS:
        supported = ", ".join(sorted(READABLE_TEXT_EXTENSIONS))
        raise error_type(f"Unsupported text file type. Supported: {supported}")
    if max_characters < 1:
        raise error_type("max_characters must be positive")
    encodings = (
        ("utf-16",) if data.startswith((b"\xff\xfe", b"\xfe\xff")) else ()
    ) + ("utf-8-sig", "cp1252")
    content = None
    used_encoding = None
    for encoding in encodings:
        try:
            content = data.decode(encoding)
            used_encoding = encoding
            break
        except UnicodeDecodeError:
            continue
    if content is None or used_encoding is None:
        raise error_type("The selected file is not valid readable text")
    if "\x00" in content:
        raise error_type("The selected file appears to contain binary data")
    truncated = len(content) > max_characters
    return content[:max_characters], used_encoding, len(content), truncated
