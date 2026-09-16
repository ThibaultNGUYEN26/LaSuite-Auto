"""Shared in-memory PDF text extraction, creation, and templating."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import reportlab
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
UNICODE_FONT_FAMILY = "AutoVera"


def _configure_unicode_fonts(pdf: FPDF) -> None:
    """Embed the Unicode-capable fonts already distributed with ReportLab."""
    font_directory = Path(reportlab.__file__).resolve().parent / "fonts"
    pdf.add_font(UNICODE_FONT_FAMILY, fname=font_directory / "Vera.ttf")
    pdf.add_font(
        UNICODE_FONT_FAMILY,
        style="B",
        fname=font_directory / "VeraBd.ttf",
    )


def _pdf_text(value: str) -> str:
    """Keep typographic separators readable when the bundled font lacks a glyph."""
    return value.translate(
        {
            ord("\u00a0"): " ",
            ord("\u00ad"): "-",
            ord("\u2010"): "-",
            ord("\u2011"): "-",
        }
    )


def extract_pdf_pages(data: bytes) -> list[str]:
    """Extract text from every PDF page while preserving empty page positions."""
    try:
        reader = PdfReader(BytesIO(data), strict=False)
        return [(page.extract_text() or "").strip() for page in reader.pages]
    except (PdfReadError, ValueError, OSError) as exc:
        raise SpecialistAgentError("Unable to read the PDF file") from exc


def read_pdf_bytes(data: bytes, *, max_characters: int) -> dict[str, Any]:
    """Read a PDF byte buffer and preserve page boundaries for citations."""
    pages = extract_pdf_pages(data)

    page_sections = [
        (page_number, f"[Page {page_number}]\n{page_text}")
        for page_number, page_text in enumerate(pages, start=1)
        if page_text
    ]
    content = "\n\n".join(section for _, section in page_sections)
    if not content.strip():
        raise SpecialistAgentError(
            "No extractable text was found (possibly a scanned/image PDF)"
        )

    truncated = len(content) > max_characters
    if truncated:
        content = content[:max_characters].rstrip()
    included_pages = [
        page_number
        for page_number, _ in page_sections
        if f"[Page {page_number}]" in content
    ]
    return {
        "content": content,
        "total_pages": len(pages),
        "pages_with_text": len(page_sections),
        "last_page_included": included_pages[-1] if included_pages else None,
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

    try:
        pdf = FPDF()
        _configure_unicode_fonts(pdf)
        pdf.set_auto_page_break(auto=True, margin=DEFAULT_MARGIN_MM)
        pdf.add_page()
        if title.strip():
            pdf.set_font(
                UNICODE_FONT_FAMILY,
                style="B",
                size=TITLE_FONT_SIZE,
            )
            pdf.multi_cell(0, 10, _pdf_text(title.strip()))
            pdf.ln(4)
        pdf.set_font(UNICODE_FONT_FAMILY, size=BODY_FONT_SIZE)
        pdf.multi_cell(0, 7, _pdf_text(body_text))
    except Exception as exc:  # pragma: no cover - fpdf raises varied exceptions
        raise PdfError("Unable to render the PDF") from exc

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
