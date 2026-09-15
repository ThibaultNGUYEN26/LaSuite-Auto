"""Shared in-memory PDF text extraction."""

from __future__ import annotations

from io import BytesIO
from typing import Any

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from agent.errors import SpecialistAgentError


def read_pdf_bytes(data: bytes, *, max_characters: int) -> dict[str, Any]:
    """Read a PDF byte buffer without creating a temporary file."""
    try:
        reader = PdfReader(BytesIO(data), strict=False)
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
    except (PdfReadError, ValueError, OSError) as exc:
        raise SpecialistAgentError("Unable to read the PDF file") from exc

    content = "\n\n".join(page for page in pages if page)
    if not content.strip():
        raise SpecialistAgentError(
            "No extractable text was found (possibly a scanned/image PDF)"
        )

    truncated = len(content) > max_characters
    if truncated:
        content = content[:max_characters]
    return {
        "content": content,
        "total_pages": len(reader.pages),
        "truncated": truncated,
    }
