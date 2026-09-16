"""Render a self-contained statistical analysis report as PDF."""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any

import reportlab
from reportlab.graphics.shapes import Drawing, Line, PolyLine, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    LongTable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
)


def _register_fonts() -> tuple[str, str]:
    regular_name = "AutoVera"
    bold_name = "AutoVeraBold"
    if regular_name not in pdfmetrics.getRegisteredFontNames():
        font_directory = Path(reportlab.__file__).resolve().parent / "fonts"
        pdfmetrics.registerFont(TTFont(regular_name, font_directory / "Vera.ttf"))
        pdfmetrics.registerFont(TTFont(bold_name, font_directory / "VeraBd.ttf"))
    return regular_name, bold_name


def _table(headers: list[str], rows: list[list[str]], regular: str, bold: str):
    values = [[Paragraph(value, ParagraphStyle("cell", fontName=bold, fontSize=8)) for value in headers]]
    values.extend(
        [Paragraph(value, ParagraphStyle("cell", fontName=regular, fontSize=8)) for value in row]
        for row in rows
    )
    result = LongTable(values, repeatRows=1, hAlign="LEFT")
    result.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EEF8")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C5D6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return result


def _trend_chart(trend: dict[str, Any], regular: str) -> Drawing:
    drawing = Drawing(235 * mm, 58 * mm)
    left, bottom, width, height = 18 * mm, 10 * mm, 205 * mm, 38 * mm
    drawing.add(Line(left, bottom, left + width, bottom, strokeColor=colors.grey))
    series = trend.get("series") or [
        {"date": trend["start"], "value": trend["first_value"]},
        {"date": trend["end"], "value": trend["last_value"]},
    ]
    values = [float(point["value"]) for point in series]
    minimum, maximum = min(values), max(values)
    span = maximum - minimum or 1.0
    points: list[float] = []
    for index, value in enumerate(values):
        points.extend(
            [
                left + index * width / max(1, len(values) - 1),
                bottom + (value - minimum) / span * height,
            ]
        )
    drawing.add(PolyLine(points, strokeColor=colors.HexColor("#2563EB"), strokeWidth=2.5))
    drawing.add(String(left, bottom + height + 5, trend["column"], fontName=regular, fontSize=10))
    drawing.add(String(left, 2, f'{trend["start"]}: {values[0]:.4g}', fontName=regular, fontSize=8))
    drawing.add(String(left + width - 80, 2, f'{trend["end"]}: {values[-1]:.4g}', fontName=regular, fontSize=8))
    return drawing


def render_pdf_report(
    analysis: dict[str, Any], *, title: str, source_name: str
) -> bytes:
    regular, bold = _register_fonts()
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "report-title", parent=styles["Title"], fontName=bold, fontSize=20
    )
    heading_style = ParagraphStyle(
        "report-heading", parent=styles["Heading2"], fontName=bold, fontSize=13
    )
    body_style = ParagraphStyle(
        "report-body", parent=styles["BodyText"], fontName=regular, fontSize=9
    )
    buffer = io.BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title=title,
    )
    story = [
        Paragraph(title, title_style),
        Paragraph(
            f'Source: {source_name} — {analysis["row_count"]} rows, '
            f'{analysis["column_count"]} columns',
            body_style,
        ),
        Spacer(1, 4 * mm),
        Paragraph("Analysis request", heading_style),
        Paragraph(analysis["question"] or "Comprehensive exploratory analysis", body_style),
    ]
    if analysis["truncated"]:
        story.append(
            Paragraph(
                "The configured row limit was reached; conclusions use the rows shown.",
                body_style,
            )
        )

    story.extend([Spacer(1, 4 * mm), Paragraph("Data quality", heading_style)])
    quality_rows = [
        [name, str(count), f'{count / analysis["row_count"] * 100:.1f}%']
        for name, count in analysis["missing"].items()
    ]
    story.append(_table(["Column", "Missing", "Missing %"], quality_rows, regular, bold))

    story.extend([Spacer(1, 4 * mm), Paragraph("Descriptive statistics", heading_style)])
    stats_rows = [
        [
            item["column"], str(item["count"]), f'{item["mean"]:.4g}',
            f'{item["median"]:.4g}', f'{item["minimum"]:.4g}',
            f'{item["maximum"]:.4g}', f'{item["standard_deviation"]:.4g}',
        ]
        for item in analysis["numeric_statistics"]
    ]
    story.append(
        _table(
            ["Column", "Count", "Mean", "Median", "Min", "Max", "Std. dev."],
            stats_rows,
            regular,
            bold,
        )
        if stats_rows
        else Paragraph("No numeric columns were detected.", body_style)
    )

    story.extend([Spacer(1, 4 * mm), Paragraph("Trends", heading_style)])
    trend_rows = [
        [
            item["column"], item["direction"], item["start"], item["end"],
            f'{item["slope_per_day"]:.4g}',
            "n/a" if item["percentage_change"] is None else f'{item["percentage_change"]:.2f}%',
            str(item["observations"]),
        ]
        for item in analysis["trends"]
    ]
    story.append(
        _table(
            ["Measure", "Direction", "Start", "End", "Slope/day", "Change", "Points"],
            trend_rows,
            regular,
            bold,
        )
        if trend_rows
        else Paragraph("No usable date-and-number combination was detected.", body_style)
    )
    for trend in analysis["trends"]:
        story.extend([Spacer(1, 3 * mm), _trend_chart(trend, regular)])

    category_rows = [
        [
            item["column"],
            str(item["unique"]),
            ", ".join(f"{name} ({count})" for name, count in item["top_values"]),
        ]
        for item in analysis["categories"]
    ]
    story.extend([Spacer(1, 4 * mm), Paragraph("Categories", heading_style)])
    story.append(
        _table(["Column", "Unique values", "Most frequent"], category_rows, regular, bold)
        if category_rows
        else Paragraph("No categorical columns were detected.", body_style)
    )

    correlation_rows = [
        [item["left"], item["right"], f'{item["correlation"]:.3f}']
        for item in sorted(
            analysis["correlations"],
            key=lambda value: abs(value["correlation"]),
            reverse=True,
        )
    ]
    story.extend([Spacer(1, 4 * mm), Paragraph("Correlations", heading_style)])
    story.append(
        _table(["First measure", "Second measure", "Pearson r"], correlation_rows, regular, bold)
        if correlation_rows
        else Paragraph("Not enough paired numeric data for correlations.", body_style)
    )
    document.build(story)
    return buffer.getvalue()
