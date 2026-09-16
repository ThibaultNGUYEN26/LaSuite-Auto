"""Dependency-free parsing, statistics, trends, charts, and HTML reporting."""

from __future__ import annotations

import csv
import html
import io
import math
import statistics
import zipfile
from collections import Counter
from datetime import datetime
from typing import Any
from xml.etree import ElementTree

from agent.errors import DataAnalysisError


DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%Y/%m/%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d-%m-%Y",
)


def parse_csv_data(data: bytes, *, max_rows: int) -> tuple[list[str], list[list[str]], bool]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise DataAnalysisError("CSV data must use UTF-8 text encoding") from exc
    if not text.strip() or "\x00" in text:
        raise DataAnalysisError("CSV data is empty or invalid")
    try:
        sample = text[:8192]
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    try:
        reader = csv.reader(io.StringIO(text), dialect)
        headers = next(reader)
        rows = []
        truncated = False
        for row in reader:
            if len(rows) >= max_rows:
                truncated = True
                break
            rows.append(row)
    except (csv.Error, StopIteration) as exc:
        raise DataAnalysisError("CSV data has no usable header row") from exc
    return _normalize_table(headers, rows), rows, truncated


def _normalize_table(
    headers: list[str], rows: list[list[str]]
) -> list[str]:
    width = max([len(headers), *(len(row) for row in rows)] or [0])
    if width == 0:
        raise DataAnalysisError("The table has no columns")
    normalized = []
    used: Counter[str] = Counter()
    for index in range(width):
        candidate = headers[index].strip() if index < len(headers) else ""
        base = candidate or f"Column {index + 1}"
        used[base] += 1
        normalized.append(base if used[base] == 1 else f"{base} ({used[base]})")
    for row in rows:
        row.extend([""] * (width - len(row)))
        del row[width:]
    return normalized


def parse_ods_data(data: bytes, *, max_rows: int) -> tuple[list[str], list[list[str]], bool]:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            content = archive.read("content.xml")
    except (zipfile.BadZipFile, KeyError) as exc:
        raise DataAnalysisError("The selected file is not a valid ODS spreadsheet") from exc
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as exc:
        raise DataAnalysisError("The ODS spreadsheet contains invalid XML") from exc

    namespaces = {
        "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
        "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
        "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    }
    table = root.find(".//table:table", namespaces)
    if table is None:
        raise DataAnalysisError("The ODS spreadsheet has no sheet")
    parsed_rows: list[list[str]] = []
    truncated = False
    for row_element in table.findall("table:table-row", namespaces):
        repeat_rows = min(
            int(row_element.get(f"{{{namespaces['table']}}}number-rows-repeated", "1")),
            max_rows + 1,
        )
        values: list[str] = []
        for cell in list(row_element):
            if cell.tag not in {
                f"{{{namespaces['table']}}}table-cell",
                f"{{{namespaces['table']}}}covered-table-cell",
            }:
                continue
            repeat_columns = min(
                int(cell.get(f"{{{namespaces['table']}}}number-columns-repeated", "1")),
                1000,
            )
            paragraphs = [
                "".join(paragraph.itertext())
                for paragraph in cell.findall("text:p", namespaces)
            ]
            value = "\n".join(paragraphs)
            if not value:
                value = cell.get(f"{{{namespaces['office']}}}value", "")
            values.extend([value] * repeat_columns)
        for _ in range(repeat_rows):
            if len(parsed_rows) >= max_rows + 1:
                truncated = True
                break
            parsed_rows.append(list(values))
        if truncated:
            break
    if not parsed_rows:
        raise DataAnalysisError("The ODS spreadsheet has no rows")
    headers, rows = parsed_rows[0], parsed_rows[1:]
    return _normalize_table(headers, rows), rows, truncated


def _number(value: str) -> float | None:
    clean = value.strip().replace("\u00a0", "").replace(" ", "")
    if not clean:
        return None
    if clean.count(",") == 1 and "." not in clean:
        clean = clean.replace(",", ".")
    elif "," in clean and "." in clean:
        clean = clean.replace(",", "")
    clean = clean.removesuffix("%")
    try:
        value_number = float(clean)
    except ValueError:
        return None
    return value_number if math.isfinite(value_number) else None


def _date(value: str) -> datetime | None:
    clean = value.strip()
    if not clean:
        return None
    try:
        return datetime.fromisoformat(clean.replace("Z", "+00:00"))
    except ValueError:
        pass
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(clean, date_format)
        except ValueError:
            continue
    return None


def _svg_chart(points: list[tuple[datetime, float]], title: str) -> str:
    width, height, padding = 760, 260, 38
    values = [value for _, value in points]
    minimum, maximum = min(values), max(values)
    span = maximum - minimum or 1.0
    coordinates = []
    for index, (_, value) in enumerate(points):
        x = padding + index * (width - 2 * padding) / max(1, len(points) - 1)
        y = height - padding - (value - minimum) * (height - 2 * padding) / span
        coordinates.append(f"{x:.1f},{y:.1f}")
    return (
        f'<figure><figcaption>{html.escape(title)}</figcaption>'
        f'<svg viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{html.escape(title)}">'
        f'<line x1="{padding}" y1="{height-padding}" x2="{width-padding}" '
        f'y2="{height-padding}" class="axis"/>'
        f'<polyline points="{" ".join(coordinates)}" class="series"/>'
        f'<text x="{padding}" y="20">max {maximum:.3g}</text>'
        f'<text x="{padding}" y="{height-8}">min {minimum:.3g}</text>'
        "</svg></figure>"
    )


def analyze_table(
    headers: list[str],
    rows: list[list[str]],
    *,
    question: str = "",
    requested_date_column: str | None = None,
    requested_value_columns: list[str] | None = None,
    truncated: bool = False,
) -> dict[str, Any]:
    if not rows:
        raise DataAnalysisError("The table contains headers but no data rows")
    columns = {header: [row[index].strip() for row in rows] for index, header in enumerate(headers)}
    missing = {name: sum(not value for value in values) for name, values in columns.items()}

    numeric: dict[str, list[float | None]] = {}
    dates: dict[str, list[datetime | None]] = {}
    for name, values in columns.items():
        nonempty = [value for value in values if value]
        if not nonempty:
            continue
        numeric_values = [_number(value) for value in values]
        date_values = [_date(value) for value in values]
        if sum(value is not None for value in numeric_values) / len(nonempty) >= 0.7:
            numeric[name] = numeric_values
        if sum(value is not None for value in date_values) / len(nonempty) >= 0.7:
            dates[name] = date_values

    statistics_rows = []
    for name, values in numeric.items():
        present = [value for value in values if value is not None]
        statistics_rows.append(
            {
                "column": name,
                "count": len(present),
                "mean": statistics.fmean(present),
                "median": statistics.median(present),
                "minimum": min(present),
                "maximum": max(present),
                "standard_deviation": statistics.stdev(present) if len(present) > 1 else 0.0,
            }
        )

    date_column = None
    if requested_date_column:
        date_column = next(
            (name for name in dates if name.casefold() == requested_date_column.casefold()),
            None,
        )
        if date_column is None:
            raise DataAnalysisError(
                f"The requested date column {requested_date_column!r} is not usable as dates"
            )
    elif dates:
        date_column = max(dates, key=lambda name: sum(value is not None for value in dates[name]))

    value_columns = list(numeric)
    if requested_value_columns:
        lookup = {name.casefold(): name for name in numeric}
        value_columns = []
        for requested in requested_value_columns:
            matched = lookup.get(requested.casefold())
            if matched is None:
                raise DataAnalysisError(
                    f"The requested value column {requested!r} is not numeric"
                )
            value_columns.append(matched)

    trends = []
    charts = []
    if date_column:
        for name in value_columns[:8]:
            points = sorted(
                (
                    (date_value, number_value)
                    for date_value, number_value in zip(dates[date_column], numeric[name])
                    if date_value is not None and number_value is not None
                ),
                key=lambda item: item[0],
            )
            if len(points) < 2:
                continue
            x_values = [point[0].timestamp() / 86400 for point in points]
            y_values = [point[1] for point in points]
            x_mean, y_mean = statistics.fmean(x_values), statistics.fmean(y_values)
            denominator = sum((value - x_mean) ** 2 for value in x_values)
            slope = (
                sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
                / denominator
                if denominator
                else 0.0
            )
            first, last = y_values[0], y_values[-1]
            percentage_change = ((last - first) / abs(first) * 100) if first else None
            tolerance = max(abs(y_mean) * 0.001, 1e-12)
            direction = "stable" if abs(slope) <= tolerance else "upward" if slope > 0 else "downward"
            chart_points = (
                points
                if len(points) <= 100
                else points[:: max(1, math.ceil(len(points) / 100))]
            )
            if chart_points[-1] != points[-1]:
                chart_points.append(points[-1])
            trends.append(
                {
                    "column": name,
                    "date_column": date_column,
                    "direction": direction,
                    "slope_per_day": slope,
                    "first_value": first,
                    "last_value": last,
                    "percentage_change": percentage_change,
                    "observations": len(points),
                    "start": points[0][0].date().isoformat(),
                    "end": points[-1][0].date().isoformat(),
                    "series": [
                        {"date": date_value.date().isoformat(), "value": number_value}
                        for date_value, number_value in chart_points
                    ],
                }
            )
            charts.append(_svg_chart(points, f"{name} over {date_column}"))

    categories = []
    for name, values in columns.items():
        if name in numeric or name in dates:
            continue
        present = [value for value in values if value]
        if present:
            categories.append(
                {
                    "column": name,
                    "unique": len(set(present)),
                    "top_values": Counter(present).most_common(5),
                }
            )

    correlations = []
    numeric_names = list(numeric)[:8]
    for left_index, left_name in enumerate(numeric_names):
        for right_name in numeric_names[left_index + 1 :]:
            pairs = [
                (left, right)
                for left, right in zip(numeric[left_name], numeric[right_name])
                if left is not None and right is not None
            ]
            if len(pairs) < 3:
                continue
            left_values, right_values = zip(*pairs)
            left_mean, right_mean = statistics.fmean(left_values), statistics.fmean(right_values)
            numerator = sum(
                (left - left_mean) * (right - right_mean)
                for left, right in pairs
            )
            denominator = math.sqrt(
                sum((left - left_mean) ** 2 for left in left_values)
                * sum((right - right_mean) ** 2 for right in right_values)
            )
            if denominator:
                correlations.append(
                    {"left": left_name, "right": right_name, "correlation": numerator / denominator}
                )

    return {
        "question": question,
        "row_count": len(rows),
        "column_count": len(headers),
        "columns": headers,
        "missing": missing,
        "numeric_statistics": statistics_rows,
        "date_column": date_column,
        "trends": trends,
        "categories": categories,
        "correlations": correlations,
        "charts": charts,
        "truncated": truncated,
    }


def render_html_report(
    analysis: dict[str, Any], *, title: str, source_name: str
) -> str:
    def table(headers: list[str], body: list[list[str]]) -> str:
        head = "".join(f"<th>{html.escape(value)}</th>" for value in headers)
        rows = "".join(
            "<tr>" + "".join(f"<td>{html.escape(value)}</td>" for value in row) + "</tr>"
            for row in body
        )
        return f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>"

    stats_body = [
        [
            item["column"], str(item["count"]), f'{item["mean"]:.4g}',
            f'{item["median"]:.4g}', f'{item["minimum"]:.4g}',
            f'{item["maximum"]:.4g}', f'{item["standard_deviation"]:.4g}',
        ]
        for item in analysis["numeric_statistics"]
    ]
    trend_body = [
        [
            item["column"], item["direction"], item["start"], item["end"],
            f'{item["slope_per_day"]:.4g}',
            "n/a" if item["percentage_change"] is None else f'{item["percentage_change"]:.2f}%',
            str(item["observations"]),
        ]
        for item in analysis["trends"]
    ]
    quality_body = [
        [name, str(count), f'{count / analysis["row_count"] * 100:.1f}%']
        for name, count in analysis["missing"].items()
    ]
    category_body = [
        [item["column"], str(item["unique"]), ", ".join(f"{name} ({count})" for name, count in item["top_values"])]
        for item in analysis["categories"]
    ]
    correlation_body = [
        [item["left"], item["right"], f'{item["correlation"]:.3f}']
        for item in sorted(analysis["correlations"], key=lambda item: abs(item["correlation"]), reverse=True)
    ]
    limitation = (
        "<p class='warning'>The configured row limit was reached; conclusions use the rows shown.</p>"
        if analysis["truncated"] else ""
    )
    question = html.escape(analysis["question"] or "Comprehensive exploratory analysis")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>{html.escape(title)}</title><style>
body{{font:15px system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 24px;color:#172033}}
h1,h2{{color:#102a43}} .meta{{color:#52606d}} table{{border-collapse:collapse;width:100%;margin:12px 0 28px}}
th,td{{border:1px solid #d9e2ec;padding:8px;text-align:left}} th{{background:#f0f4f8}}
figure{{margin:24px 0}} figcaption{{font-weight:650;margin-bottom:8px}} svg{{width:100%;background:#f8fafc}}
.axis{{stroke:#829ab1}} .series{{fill:none;stroke:#2563eb;stroke-width:3}} .warning{{background:#fff3cd;padding:12px}}
</style></head><body><h1>{html.escape(title)}</h1>
<p class="meta">Source: {html.escape(source_name)} · {analysis["row_count"]} rows · {analysis["column_count"]} columns</p>
<p><strong>Analysis request:</strong> {question}</p>{limitation}
<h2>Data quality</h2>{table(["Column", "Missing", "Missing %"], quality_body)}
<h2>Descriptive statistics</h2>{table(["Column", "Count", "Mean", "Median", "Min", "Max", "Std. dev."], stats_body) if stats_body else "<p>No numeric columns were detected.</p>"}
<h2>Trends</h2>{table(["Measure", "Direction", "Start", "End", "Slope/day", "Change", "Points"], trend_body) if trend_body else "<p>No usable date-and-number combination was detected.</p>"}
{"".join(analysis["charts"])}
<h2>Categories</h2>{table(["Column", "Unique values", "Most frequent"], category_body) if category_body else "<p>No categorical columns were detected.</p>"}
<h2>Correlations</h2>{table(["First measure", "Second measure", "Pearson r"], correlation_body) if correlation_body else "<p>Not enough paired numeric data for correlations.</p>"}
</body></html>"""
