"""Dependency-free parsing and comprehensive statistical analysis."""

from __future__ import annotations

import csv
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


def parse_csv_data(
    data: bytes, *, max_rows: int
) -> tuple[list[str], list[list[str]], bool]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise DataAnalysisError("CSV data must use UTF-8 text encoding") from exc
    if not text.strip() or "\x00" in text:
        raise DataAnalysisError("CSV data is empty or invalid")
    try:
        dialect = csv.Sniffer().sniff(text[:8192], delimiters=",;\t|")
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


def _normalize_table(headers: list[str], rows: list[list[str]]) -> list[str]:
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


def parse_ods_data(
    data: bytes, *, max_rows: int
) -> tuple[list[str], list[list[str]], bool]:
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
            int(
                row_element.get(
                    f"{{{namespaces['table']}}}number-rows-repeated", "1"
                )
            ),
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
                int(
                    cell.get(
                        f"{{{namespaces['table']}}}number-columns-repeated", "1"
                    )
                ),
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
        number = float(clean)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


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


def _percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def _pearson(left_values: list[float], right_values: list[float]) -> float | None:
    if len(left_values) < 3 or len(left_values) != len(right_values):
        return None
    left_mean = statistics.fmean(left_values)
    right_mean = statistics.fmean(right_values)
    numerator = sum(
        (left - left_mean) * (right - right_mean)
        for left, right in zip(left_values, right_values)
    )
    denominator = math.sqrt(
        sum((left - left_mean) ** 2 for left in left_values)
        * sum((right - right_mean) ** 2 for right in right_values)
    )
    return numerator / denominator if denominator else None


def _correlation_strength(value: float) -> str:
    magnitude = abs(value)
    if magnitude >= 0.8:
        return "very strong"
    if magnitude >= 0.6:
        return "strong"
    if magnitude >= 0.4:
        return "moderate"
    if magnitude >= 0.2:
        return "weak"
    return "very weak"


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

    columns = {
        header: [row[index].strip() for row in rows]
        for index, header in enumerate(headers)
    }
    missing = {
        name: sum(not value for value in values)
        for name, values in columns.items()
    }
    duplicate_rows = len(rows) - len({tuple(row) for row in rows})
    total_cells = len(rows) * len(headers)
    missing_cells = sum(missing.values())

    numeric: dict[str, list[float | None]] = {}
    dates: dict[str, list[datetime | None]] = {}
    invalid_numeric: dict[str, int] = {}
    for name, values in columns.items():
        nonempty = [value for value in values if value]
        if not nonempty:
            continue
        numeric_values = [_number(value) for value in values]
        date_values = [_date(value) for value in values]
        if sum(value is not None for value in numeric_values) / len(nonempty) >= 0.7:
            numeric[name] = numeric_values
            invalid_numeric[name] = sum(
                bool(raw) and parsed is None
                for raw, parsed in zip(values, numeric_values)
            )
        if sum(value is not None for value in date_values) / len(nonempty) >= 0.7:
            dates[name] = date_values

    statistics_rows = []
    for name, values in numeric.items():
        present = [value for value in values if value is not None]
        first_quartile = _percentile(present, 0.25)
        third_quartile = _percentile(present, 0.75)
        interquartile_range = third_quartile - first_quartile
        lower_fence = first_quartile - 1.5 * interquartile_range
        upper_fence = third_quartile + 1.5 * interquartile_range
        outliers = [
            value for value in present if value < lower_fence or value > upper_fence
        ]
        mean = statistics.fmean(present)
        deviation = statistics.stdev(present) if len(present) > 1 else 0.0
        statistics_rows.append(
            {
                "column": name,
                "count": len(present),
                "missing": missing[name],
                "invalid": invalid_numeric[name],
                "sum": sum(present),
                "mean": mean,
                "median": statistics.median(present),
                "minimum": min(present),
                "first_quartile": first_quartile,
                "third_quartile": third_quartile,
                "maximum": max(present),
                "standard_deviation": deviation,
                "coefficient_of_variation": deviation / abs(mean) if mean else None,
                "outlier_count": len(outliers),
                "outlier_examples": sorted(outliers, key=abs, reverse=True)[:5],
            }
        )

    date_column = None
    if requested_date_column:
        date_column = next(
            (
                name
                for name in dates
                if name.casefold() == requested_date_column.casefold()
            ),
            None,
        )
        if date_column is None:
            raise DataAnalysisError(
                f"The requested date column {requested_date_column!r} is not usable as dates"
            )
    elif dates:
        date_column = max(
            dates,
            key=lambda name: sum(value is not None for value in dates[name]),
        )

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
    if date_column:
        for name in value_columns[:8]:
            points = sorted(
                (
                    (date_value, number_value)
                    for date_value, number_value in zip(
                        dates[date_column], numeric[name]
                    )
                    if date_value is not None and number_value is not None
                ),
                key=lambda item: item[0],
            )
            if len(points) < 2:
                continue
            x_values = [point[0].timestamp() / 86400 for point in points]
            y_values = [point[1] for point in points]
            x_mean = statistics.fmean(x_values)
            y_mean = statistics.fmean(y_values)
            denominator = sum((value - x_mean) ** 2 for value in x_values)
            slope = (
                sum(
                    (x - x_mean) * (y - y_mean)
                    for x, y in zip(x_values, y_values)
                )
                / denominator
                if denominator
                else 0.0
            )
            first, last = y_values[0], y_values[-1]
            percentage_change = (
                (last - first) / abs(first) * 100 if first else None
            )
            fitted = [y_mean + slope * (value - x_mean) for value in x_values]
            total_variation = sum((value - y_mean) ** 2 for value in y_values)
            residual_variation = sum(
                (value - estimate) ** 2
                for value, estimate in zip(y_values, fitted)
            )
            r_squared = (
                1 - residual_variation / total_variation
                if total_variation
                else 1.0
            )
            changes = [
                {
                    "start": points[index - 1][0].date().isoformat(),
                    "end": points[index][0].date().isoformat(),
                    "absolute_change": current - previous,
                    "percentage_change": (
                        (current - previous) / abs(previous) * 100
                        if previous
                        else None
                    ),
                }
                for index, (previous, current) in enumerate(
                    zip(y_values, y_values[1:]), start=1
                )
            ]
            percentage_changes = [
                change["percentage_change"]
                for change in changes
                if change["percentage_change"] is not None
            ]
            duration_years = (
                points[-1][0] - points[0][0]
            ).total_seconds() / (365.2425 * 86400)
            annualized_change = None
            if duration_years > 0 and first > 0 and last > 0:
                annualized_change = (
                    (last / first) ** (1 / duration_years) - 1
                ) * 100
            fitted_movement = slope * (x_values[-1] - x_values[0])
            tolerance = max(abs(y_mean) * 0.01, 1e-12)
            direction = (
                "stable"
                if abs(fitted_movement) <= tolerance
                else "upward" if fitted_movement > 0 else "downward"
            )
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
                    "annualized_change": annualized_change,
                    "r_squared": max(0.0, min(1.0, r_squared)),
                    "average_period_change": (
                        statistics.fmean(percentage_changes)
                        if percentage_changes
                        else None
                    ),
                    "period_change_volatility": (
                        statistics.stdev(percentage_changes)
                        if len(percentage_changes) > 1
                        else 0.0 if percentage_changes else None
                    ),
                    "largest_increase": max(
                        changes, key=lambda value: value["absolute_change"]
                    ),
                    "largest_decrease": min(
                        changes, key=lambda value: value["absolute_change"]
                    ),
                    "observations": len(points),
                    "start": points[0][0].date().isoformat(),
                    "end": points[-1][0].date().isoformat(),
                    "series": [
                        {
                            "date": date_value.date().isoformat(),
                            "value": number_value,
                        }
                        for date_value, number_value in chart_points
                    ],
                }
            )

    categories = []
    for name, values in columns.items():
        if name in numeric or name in dates:
            continue
        present = [value for value in values if value]
        if present:
            top_values = Counter(present).most_common(10)
            categories.append(
                {
                    "column": name,
                    "unique": len(set(present)),
                    "top_values": top_values,
                    "most_common_share": top_values[0][1] / len(present),
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
            correlation = _pearson(list(left_values), list(right_values))
            if correlation is not None:
                correlations.append(
                    {
                        "left": left_name,
                        "right": right_name,
                        "correlation": correlation,
                        "strength": _correlation_strength(correlation),
                        "observations": len(pairs),
                    }
                )

    findings = []
    for trend in trends:
        change = trend["percentage_change"]
        change_text = f" ({change:+.1f}% overall)" if change is not None else ""
        findings.append(
            f'{trend["column"]} shows a {trend["direction"]} trajectory from '
            f'{trend["start"]} to {trend["end"]}{change_text}; the linear trend '
            f'explains {trend["r_squared"] * 100:.1f}% of observed variation.'
        )
    strongest = sorted(
        correlations,
        key=lambda value: abs(value["correlation"]),
        reverse=True,
    )[:3]
    for item in strongest:
        if abs(item["correlation"]) >= 0.4:
            relationship = "positive" if item["correlation"] > 0 else "negative"
            findings.append(
                f'{item["left"]} and {item["right"]} have a '
                f'{item["strength"]} {relationship} association '
                f'(r={item["correlation"]:.2f}, n={item["observations"]}).'
            )
    outlier_columns = [
        f'{item["column"]} ({item["outlier_count"]})'
        for item in statistics_rows
        if item["outlier_count"]
    ]
    if outlier_columns:
        findings.append(
            "Potential IQR outliers were detected in "
            + ", ".join(outlier_columns)
            + "."
        )
    if duplicate_rows or missing_cells:
        findings.append(
            f"Data quality review found {duplicate_rows} duplicate rows and "
            f"{missing_cells} missing cells out of {total_cells}."
        )
    if not findings:
        findings.append(
            "The available data does not contain enough variation or time structure "
            "for a reliable trend or relationship finding."
        )

    limitations = [
        "Associations and trends are descriptive and do not establish causality.",
        "Results depend on the accuracy, definitions, and collection process of the source data.",
    ]
    if truncated:
        limitations.insert(
            0,
            "The configured row limit was reached, so conclusions cover only the analyzed rows.",
        )
    if len(rows) < 30:
        limitations.append(
            f"The analysis contains only {len(rows)} rows; estimates may be sensitive to individual observations."
        )
    invalid_total = sum(invalid_numeric.values())
    if invalid_total:
        limitations.append(
            f"{invalid_total} non-empty values in numeric columns could not be parsed and were excluded."
        )

    return {
        "question": question,
        "row_count": len(rows),
        "column_count": len(headers),
        "columns": headers,
        "missing": missing,
        "quality": {
            "total_cells": total_cells,
            "missing_cells": missing_cells,
            "completeness": (
                1 - missing_cells / total_cells if total_cells else 0.0
            ),
            "duplicate_rows": duplicate_rows,
            "duplicate_rate": duplicate_rows / len(rows),
            "invalid_numeric_values": invalid_numeric,
        },
        "numeric_statistics": statistics_rows,
        "date_column": date_column,
        "trends": trends,
        "categories": categories,
        "correlations": correlations,
        "findings": findings,
        "limitations": limitations,
        "truncated": truncated,
    }
