"""Deterministic PDF rendering for structured audit artifacts."""

from __future__ import annotations

from collections import Counter
from html import escape
from io import BytesIO
from pathlib import Path
from typing import Any

import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from agent.errors import PdfError


FONT_FAMILY = "AutoVera"


def _register_fonts() -> None:
    registered = pdfmetrics.getRegisteredFontNames()
    font_directory = Path(reportlab.__file__).resolve().parent / "fonts"
    if FONT_FAMILY not in registered:
        pdfmetrics.registerFont(TTFont(FONT_FAMILY, font_directory / "Vera.ttf"))
    if f"{FONT_FAMILY}-Bold" not in registered:
        pdfmetrics.registerFont(
            TTFont(f"{FONT_FAMILY}-Bold", font_directory / "VeraBd.ttf")
        )
    pdfmetrics.registerFontFamily(
        FONT_FAMILY,
        normal=FONT_FAMILY,
        bold=f"{FONT_FAMILY}-Bold",
        italic=FONT_FAMILY,
        boldItalic=f"{FONT_FAMILY}-Bold",
    )


def _paragraph_text(value: object) -> str:
    return escape(str(value or "")).replace("\n", "<br/>")


def _validate_payload(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    findings = payload.get("findings")
    sources = payload.get("sources")
    if not isinstance(findings, list) or not findings:
        raise PdfError("The audit artifact contains no structured findings")
    if not isinstance(sources, list) or not sources:
        raise PdfError("The audit artifact contains no source register")
    if not all(isinstance(item, dict) for item in findings):
        raise PdfError("The audit artifact contains invalid findings")
    if not all(isinstance(item, dict) for item in sources):
        raise PdfError("The audit artifact contains an invalid source register")
    return findings, sources


def render_audit_report(payload: dict[str, Any], *, title: str) -> tuple[bytes, dict[str, Any]]:
    """Render every structured finding and source without a text-size ceiling."""
    findings, sources = _validate_payload(payload)
    _register_fonts()

    statuses = Counter(str(item.get("status") or "UNKNOWN") for item in findings)
    overall_result = str(payload.get("overall_result") or "")
    if not overall_result:
        overall_result = (
            "NON-COMPLIANT"
            if statuses["NON-COMPLIANT"]
            else "INCOMPLETE — INSUFFICIENT EVIDENCE"
            if statuses["INSUFFICIENT EVIDENCE"]
            else "COMPLIANT"
        )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "AuditTitle",
        parent=styles["Title"],
        fontName=f"{FONT_FAMILY}-Bold",
        fontSize=20,
        leading=25,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=14,
    )
    heading_style = ParagraphStyle(
        "AuditHeading",
        parent=styles["Heading1"],
        fontName=f"{FONT_FAMILY}-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#17365D"),
        spaceBefore=8,
        spaceAfter=8,
    )
    finding_style = ParagraphStyle(
        "AuditFinding",
        parent=styles["Heading2"],
        fontName=f"{FONT_FAMILY}-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#244A73"),
        spaceBefore=10,
        spaceAfter=5,
    )
    body_style = ParagraphStyle(
        "AuditBody",
        parent=styles["BodyText"],
        fontName=FONT_FAMILY,
        fontSize=8.5,
        leading=11.5,
        spaceAfter=5,
        splitLongWords=True,
    )
    label_style = ParagraphStyle(
        "AuditLabel",
        parent=body_style,
        fontName=f"{FONT_FAMILY}-Bold",
        spaceAfter=2,
    )

    output = BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=title,
        author="Auto — La Suite Automations",
    )

    def footer(canvas: Any, doc: Any) -> None:
        canvas.saveState()
        canvas.setFont(FONT_FAMILY, 7)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(16 * mm, 9 * mm, "Audit working document")
        canvas.drawRightString(A4[0] - 16 * mm, 9 * mm, f"Page {doc.page}")
        canvas.restoreState()

    story: list[Any] = [
        Spacer(1, 18 * mm),
        Paragraph(_paragraph_text(title), title_style),
        Paragraph(
            _paragraph_text(payload.get("client_directory") or "Audit evidence corpus"),
            ParagraphStyle(
                "AuditSubtitle",
                parent=body_style,
                fontSize=10,
                leading=14,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#555555"),
            ),
        ),
        Spacer(1, 12 * mm),
        Paragraph("Overall result", heading_style),
        Paragraph(f"<b>{_paragraph_text(overall_result)}</b>", body_style),
        Paragraph(f"Criteria assessed: {len(findings)}", body_style),
        Paragraph(f"Compliant: {statuses['COMPLIANT']}", body_style),
        Paragraph(f"Non-compliant: {statuses['NON-COMPLIANT']}", body_style),
        Paragraph(
            f"Insufficient evidence: {statuses['INSUFFICIENT EVIDENCE']}",
            body_style,
        ),
        Paragraph(f"Registered sources: {len(sources)}", body_style),
        PageBreak(),
        Paragraph("Source register", heading_style),
        Paragraph(
            "Use each source ID and exact location to reopen the evidence. "
            "PDF citations identify pages; CSV and text citations identify lines.",
            body_style,
        ),
    ]

    for source in sources:
        source_id = _paragraph_text(source.get("source_id") or "SOURCE")
        name = _paragraph_text(source.get("name") or "Unnamed source")
        story.extend(
            (
                Paragraph(f"<b>{source_id} — {name}</b>", finding_style),
                Paragraph(
                    "<b>Role:</b> " + _paragraph_text(source.get("role")),
                    body_style,
                ),
                Paragraph(
                    "<b>Type:</b> " + _paragraph_text(source.get("type")),
                    body_style,
                ),
                Paragraph(
                    "<b>Exact location:</b> "
                    + _paragraph_text(source.get("relative_path")),
                    body_style,
                ),
                Paragraph(
                    "<b>Retrieval:</b> " + _paragraph_text(source.get("retrieval")),
                    body_style,
                ),
            )
        )

    story.extend((PageBreak(), Paragraph("Complete audit findings", heading_style)))
    fields = (
        ("Requirement", "requirement"),
        ("Reference evidence", "reference_evidence"),
        ("Client evidence", "client_evidence"),
        ("Reasoning", "reasoning"),
        ("Corrective action", "corrective_action"),
    )
    for index, finding in enumerate(findings, start=1):
        number = finding.get("criterion_number") or index
        name = finding.get("name") or f"Criterion {number}"
        status = finding.get("status") or "UNKNOWN"
        story.extend(
            (
                Paragraph(
                    f"Criterion {number}: {_paragraph_text(name)}",
                    finding_style,
                ),
                Paragraph(f"<b>Verdict:</b> {_paragraph_text(status)}", body_style),
            )
        )
        for label, key in fields:
            story.append(Paragraph(_paragraph_text(label), label_style))
            story.append(Paragraph(_paragraph_text(finding.get(key)), body_style))

    limitations = payload.get("limitations")
    story.extend((PageBreak(), Paragraph("Limitations", heading_style)))
    if isinstance(limitations, list) and limitations:
        for limitation in limitations:
            story.append(Paragraph("• " + _paragraph_text(limitation), body_style))
    else:
        story.append(
            Paragraph(
                "No technical corpus limitation was reported for this audit.",
                body_style,
            )
        )

    try:
        document.build(story, onFirstPage=footer, onLaterPages=footer)
    except Exception as exc:  # pragma: no cover - ReportLab raises varied errors
        raise PdfError("Unable to render the structured audit PDF") from exc

    return output.getvalue(), {
        "criteria_count": len(findings),
        "source_register_count": len(sources),
        "verdict_counts": dict(statuses),
        "overall_result": overall_result,
        "complete": bool(payload.get("complete", not limitations)),
    }


__all__ = ["render_audit_report"]
