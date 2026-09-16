"""Shared in-memory PDF text extraction, creation, and templating."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import typst
from fpdf import FPDF
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from agent.artifacts import Artifact
from agent.errors import PdfError, SpecialistAgentError
from services.local_files import prepare_new_local_file

DEFAULT_MARGIN_MM = 15
TITLE_FONT_SIZE = 16
BODY_FONT_SIZE = 11


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


def _write_pdf_file(content: bytes, target: Path) -> int:
    try:
        with target.open("xb") as file:
            file.write(content)
    except FileExistsError as exc:
        raise PdfError(
            "A file with this name already exists. Choose another name."
        ) from exc
    except PermissionError as exc:
        raise PdfError("Permission denied") from exc
    return len(content)


def _write_pdf_bytes(pdf: FPDF, target: Path) -> int:
    try:
        content = bytes(pdf.output())
    except Exception as exc:  # pragma: no cover - fpdf raises varied exceptions
        raise PdfError("Unable to render the PDF") from exc
    return _write_pdf_file(content, target)


def _file_artifact(relative_path: str, name: str) -> dict[str, Any]:
    return Artifact(
        kind="file",
        location="local",
        reference=relative_path,
        media_type="application/pdf",
        name=name,
    ).tool_value()


def create_local_pdf(
    root: Path,
    *,
    directory: str,
    file_name: str,
    title: str,
    body_text: str,
    max_body_characters: int,
) -> dict[str, Any]:
    """Create a simple single-column PDF with an optional title and body text."""
    if len(body_text) > max_body_characters:
        raise PdfError(
            f"body_text exceeds the configured {max_body_characters}-character limit"
        )
    target, relative_path = prepare_new_local_file(
        root, directory=directory, file_name=file_name, extension="pdf"
    )

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=DEFAULT_MARGIN_MM)
    pdf.add_page()
    if title.strip():
        pdf.set_font("Helvetica", style="B", size=TITLE_FONT_SIZE)
        pdf.multi_cell(0, 10, title.strip())
        pdf.ln(4)
    pdf.set_font("Helvetica", size=BODY_FONT_SIZE)
    pdf.multi_cell(0, 7, body_text)

    bytes_written = _write_pdf_bytes(pdf, target)
    return {
        "status": "created",
        "relative_path": relative_path,
        "bytes_written": bytes_written,
        "artifact": _file_artifact(relative_path, target.name),
    }


def render_typst_template_to_local_pdf(
    root: Path,
    *,
    source_path: Path,
    directory: str,
    file_name: str,
) -> dict[str, Any]:
    """Compile a local Typst (.typ) template into a PDF.

    Layout - headers, footers, page numbers, styling - lives in the template
    itself via Typst's own markup, so there is nothing to pass in beyond the
    source file and destination.
    """
    target, relative_path = prepare_new_local_file(
        root, directory=directory, file_name=file_name, extension="pdf"
    )
    try:
        content = typst.compile(str(source_path), root=str(root))
    except Exception as exc:
        raise PdfError("Unable to compile the Typst template") from exc

    bytes_written = _write_pdf_file(content, target)
    return {
        "status": "created",
        "relative_path": relative_path,
        "bytes_written": bytes_written,
        "artifact": _file_artifact(relative_path, target.name),
    }
