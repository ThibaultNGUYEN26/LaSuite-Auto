"""Render a comprehensive statistical analysis report as PDF."""

from __future__ import annotations

import io
from html import escape
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
    PageBreak,
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


def _text(value: Any) -> str:
    return escape(str(value))


def _number(value: float | None, *, percentage: bool = False) -> str:
    if value is None:
        return "n/a"
    suffix = "%" if percentage else ""
    return f"{value:,.4g}{suffix}"


def _table(
    headers: list[str], rows: list[list[str]], regular: str, bold: str
) -> LongTable:
    cell_style = ParagraphStyle(
        "report-cell", fontName=regular, fontSize=7.5, leading=9
    )
    header_style = ParagraphStyle(
        "report-cell-header", fontName=bold, fontSize=7.5, leading=9
    )
    values = [
        [Paragraph(_text(value), header_style) for value in headers]
    ]
    values.extend(
        [Paragraph(_text(value), cell_style) for value in row]
        for row in rows
    )
    result = LongTable(values, repeatRows=1, hAlign="LEFT")
    result.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE8F7")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FC")]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C5D6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return result


def _trend_chart(trend: dict[str, Any], regular: str) -> Drawing:
    drawing = Drawing(235 * mm, 62 * mm)
    left, bottom, width, height = 18 * mm, 12 * mm, 205 * mm, 40 * mm
    drawing.add(Line(left, bottom, left + width, bottom, strokeColor=colors.grey))
    drawing.add(Line(left, bottom, left, bottom + height, strokeColor=colors.grey))
    series = trend["series"]
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
    drawing.add(
        PolyLine(points, strokeColor=colors.HexColor("#2563EB"), strokeWidth=2.5)
    )
    drawing.add(
        String(
            left,
            bottom + height + 7,
            str(trend["column"]),
            fontName=regular,
            fontSize=10,
        )
    )
    drawing.add(
        String(
            left,
            2,
            f'{trend["start"]}: {values[0]:.4g}',
            fontName=regular,
            fontSize=8,
        )
    )
    drawing.add(
        String(
            left + width - 90,
            2,
            f'{trend["end"]}: {values[-1]:.4g}',
            fontName=regular,
            fontSize=8,
        )
    )
    drawing.add(
        String(
            1,
            bottom + height,
            f"max {maximum:.4g}",
            fontName=regular,
            fontSize=7,
        )
    )
    drawing.add(
        String(
            1,
            bottom,
            f"min {minimum:.4g}",
            fontName=regular,
            fontSize=7,
        )
    )
    return drawing


def _page_number(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52606D"))
    canvas.drawRightString(
        landscape(A4)[0] - 16 * mm,
        8 * mm,
        f"Page {document.page}",
    )
    canvas.restoreState()


def render_pdf_report(
    analysis: dict[str, Any], *, title: str, source_name: str
) -> bytes:
    regular, bold = _register_fonts()
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "report-title", parent=styles["Title"], fontName=bold, fontSize=20
    )
    heading_style = ParagraphStyle(
        "report-heading",
        parent=styles["Heading2"],
        fontName=bold,
        fontSize=13,
        spaceBefore=7,
        spaceAfter=5,
        textColor=colors.HexColor("#102A43"),
    )
    subheading_style = ParagraphStyle(
        "report-subheading",
        parent=styles["Heading3"],
        fontName=bold,
        fontSize=10,
        spaceBefore=5,
        spaceAfter=3,
    )
    body_style = ParagraphStyle(
        "report-body", parent=styles["BodyText"], fontName=regular, fontSize=9, leading=12
    )
    bullet_style = ParagraphStyle(
        "report-bullet",
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-7,
        spaceAfter=3,
    )
    note_style = ParagraphStyle(
        "report-note",
        parent=body_style,
        backColor=colors.HexColor("#FFF4CC"),
        borderPadding=6,
        spaceBefore=5,
        spaceAfter=5,
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
        author="Auto data analyst",
        subject=analysis["question"],
    )
    quality = analysis["quality"]
    story = [
        Paragraph(_text(title), title_style),
        Paragraph(
            f"<b>Source:</b> {_text(source_name)}<br/>"
            f'<b>Scope:</b> {analysis["row_count"]:,} rows, '
            f'{analysis["column_count"]:,} columns<br/>'
            f"<b>Question:</b> {_text(analysis['question'] or 'Comprehensive exploratory analysis')}",
            body_style,
        ),
        Spacer(1, 3 * mm),
        Paragraph("Executive summary", heading_style),
    ]
    for finding in analysis["findings"]:
        story.append(Paragraph("• " + _text(finding), bullet_style))
    if analysis["truncated"]:
        story.append(
            Paragraph(
                "Important: the row limit was reached. Findings cover the analyzed subset only.",
                note_style,
            )
        )

    story.extend(
        [
            Paragraph("Data quality and coverage", heading_style),
            _table(
                ["Indicator", "Result"],
                [
                    ["Completeness", f'{quality["completeness"] * 100:.2f}%'],
                    ["Missing cells", f'{quality["missing_cells"]:,} / {quality["total_cells"]:,}'],
                    ["Duplicate rows", f'{quality["duplicate_rows"]:,} ({quality["duplicate_rate"] * 100:.2f}%)'],
                    ["Detected date column", analysis["date_column"] or "None"],
                ],
                regular,
                bold,
            ),
            Spacer(1, 2 * mm),
            _table(
                ["Column", "Missing", "Missing %", "Invalid numeric"],
                [
                    [
                        name,
                        str(count),
                        f'{count / analysis["row_count"] * 100:.2f}%',
                        str(quality["invalid_numeric_values"].get(name, 0)),
                    ]
                    for name, count in analysis["missing"].items()
                ],
                regular,
                bold,
            ),
            Paragraph("Numeric distributions", heading_style),
        ]
    )

    statistics_rows = [
        [
            item["column"],
            str(item["count"]),
            _number(item["sum"]),
            _number(item["mean"]),
            _number(item["median"]),
            _number(item["minimum"]),
            _number(item["first_quartile"]),
            _number(item["third_quartile"]),
            _number(item["maximum"]),
            _number(item["standard_deviation"]),
            _number(
                item["coefficient_of_variation"] * 100
                if item["coefficient_of_variation"] is not None
                else None,
                percentage=True,
            ),
            str(item["outlier_count"]),
        ]
        for item in analysis["numeric_statistics"]
    ]
    story.append(
        _table(
            [
                "Measure",
                "N",
                "Sum",
                "Mean",
                "Median",
                "Min",
                "Q1",
                "Q3",
                "Max",
                "Std. dev.",
                "CV",
                "IQR outliers",
            ],
            statistics_rows,
            regular,
            bold,
        )
        if statistics_rows
        else Paragraph("No numeric columns were detected.", body_style)
    )

    story.extend([PageBreak(), Paragraph("Time-series analysis", heading_style)])
    if not analysis["trends"]:
        story.append(
            Paragraph(
                "No usable date-and-number combination was detected for trend analysis.",
                body_style,
            )
        )
    for trend in analysis["trends"]:
        story.extend(
            [
                Paragraph(_text(trend["column"]), subheading_style),
                _table(
                    [
                        "Direction",
                        "Period",
                        "Overall change",
                        "Annualized",
                        "Slope/day",
                        "Trend fit (R²)",
                        "Avg. period change",
                        "Volatility",
                        "N",
                    ],
                    [[
                        trend["direction"],
                        f'{trend["start"]} to {trend["end"]}',
                        _number(trend["percentage_change"], percentage=True),
                        _number(trend["annualized_change"], percentage=True),
                        _number(trend["slope_per_day"]),
                        f'{trend["r_squared"]:.3f}',
                        _number(trend["average_period_change"], percentage=True),
                        _number(trend["period_change_volatility"], percentage=True),
                        str(trend["observations"]),
                    ]],
                    regular,
                    bold,
                ),
                Paragraph(
                    "Largest increase: "
                    f'{trend["largest_increase"]["start"]} to '
                    f'{trend["largest_increase"]["end"]} '
                    f'({_number(trend["largest_increase"]["absolute_change"])}, '
                    f'{_number(trend["largest_increase"]["percentage_change"], percentage=True)}). '
                    "Largest decrease: "
                    f'{trend["largest_decrease"]["start"]} to '
                    f'{trend["largest_decrease"]["end"]} '
                    f'({_number(trend["largest_decrease"]["absolute_change"])}, '
                    f'{_number(trend["largest_decrease"]["percentage_change"], percentage=True)}).',
                    body_style,
                ),
                _trend_chart(trend, regular),
            ]
        )

    category_rows = [
        [
            item["column"],
            str(item["unique"]),
            f'{item["most_common_share"] * 100:.1f}%',
            ", ".join(
                f"{name} ({count})" for name, count in item["top_values"]
            ),
        ]
        for item in analysis["categories"]
    ]
    story.extend([PageBreak(), Paragraph("Categorical structure", heading_style)])
    story.append(
        _table(
            ["Column", "Unique values", "Top share", "Most frequent values"],
            category_rows,
            regular,
            bold,
        )
        if category_rows
        else Paragraph("No categorical columns were detected.", body_style)
    )

    correlation_rows = [
        [
            item["left"],
            item["right"],
            f'{item["correlation"]:.3f}',
            item["strength"],
            str(item["observations"]),
        ]
        for item in sorted(
            analysis["correlations"],
            key=lambda value: abs(value["correlation"]),
            reverse=True,
        )
    ]
    story.extend([Paragraph("Relationships between measures", heading_style)])
    story.append(
        _table(
            ["First measure", "Second measure", "Pearson r", "Strength", "Paired N"],
            correlation_rows,
            regular,
            bold,
        )
        if correlation_rows
        else Paragraph("Not enough paired numeric data for correlations.", body_style)
    )

    story.extend(
        [
            Paragraph("Methodology", heading_style),
            Paragraph(
                "Numeric summaries include count, sum, mean, median, quartiles, range, "
                "sample standard deviation, coefficient of variation, and Tukey IQR "
                "outlier detection. Time trends use ordinary least-squares regression "
                "against elapsed days; R² indicates how much variation is explained by "
                "that linear trend. Period changes, volatility, largest movements, and "
                "annualized growth are calculated when the data supports them. "
                "Relationships use Pearson correlation on paired non-missing values.",
                body_style,
            ),
            Paragraph("Limitations and interpretation", heading_style),
        ]
    )
    for limitation in analysis["limitations"]:
        story.append(Paragraph("• " + _text(limitation), bullet_style))

    document.build(story, onFirstPage=_page_number, onLaterPages=_page_number)
    return buffer.getvalue()
