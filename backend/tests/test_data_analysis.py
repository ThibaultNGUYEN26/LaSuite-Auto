import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from pypdf import PdfReader

from agent.base import DelegationContext
from agent.specialists.data_analysis import AnalyzeTableAgent
from services.grist import read_grist_table
from services.tabular_analysis import parse_ods_data


class DataAnalysisAgentTests(unittest.TestCase):
    def test_analyzes_local_csv_and_creates_report_with_trend_chart(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "sales.csv").write_text(
                "date,revenue,orders,region\n"
                "2026-01-01,100,4,North\n"
                "2026-02-01,130,5,South\n"
                "2026-03-01,180,8,North\n",
                encoding="utf-8",
            )
            agent = AnalyzeTableAgent(
                local_files_root=root,
                drive_base_url="http://drive:8071",
                drive_session_id="session",
                grist_base_url="http://grist:8484",
                grist_api_key="key",
            )

            result = agent.execute(
                {
                    "artifact": {
                        "kind": "file",
                        "location": "local",
                        "reference": "sales.csv",
                        "media_type": "text/csv",
                        "name": "sales.csv",
                        "metadata": {},
                    },
                    "question": "What is the revenue tendency over time?",
                    "report_name": "sales-analysis",
                    "report_format": "html",
                    "date_column": "date",
                    "value_columns": ["revenue"],
                },
                DelegationContext(conversation=()),
            )

            self.assertEqual(result["status"], "analyzed")
            self.assertEqual(result["rows_analyzed"], 3)
            self.assertEqual(result["trends"][0]["direction"], "upward")
            self.assertGreater(result["trends"][0]["percentage_change"], 79)
            self.assertEqual(result["artifact"]["media_type"], "text/html")
            report = (root / "sales-analysis.html").read_text(encoding="utf-8")
            self.assertIn("What is the revenue tendency over time?", report)
            self.assertIn("<svg", report)
            self.assertIn("upward", report)

    def test_creates_a_pdf_report_by_default(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "activité.csv").write_text(
                "date,surface\n"
                "2024-01-01,42.5\n"
                "2025-01-01,48.7\n",
                encoding="utf-8-sig",
            )
            agent = AnalyzeTableAgent(
                local_files_root=root,
                drive_base_url="http://drive:8071",
                drive_session_id="session",
                grist_base_url="http://grist:8484",
                grist_api_key="key",
            )

            result = agent.execute(
                {
                    "artifact": {
                        "kind": "file",
                        "location": "local",
                        "reference": "activité.csv",
                        "media_type": "text/csv",
                        "name": "activité.csv",
                        "metadata": {},
                    },
                    "question": "Quelle est l'évolution de la surface pâturale ?",
                    "report_name": "rapport-pâturage",
                },
                DelegationContext(conversation=()),
            )

            report_path = root / "rapport-pâturage.pdf"
            self.assertEqual(result["report_format"], "pdf")
            self.assertEqual(result["artifact"]["media_type"], "application/pdf")
            self.assertTrue(report_path.read_bytes().startswith(b"%PDF-"))
            extracted = "".join(
                page.extract_text() or "" for page in PdfReader(report_path).pages
            )
            self.assertIn("évolution", extracted)
            self.assertIn("Trends", extracted)

    def test_parses_first_sheet_from_an_ods_spreadsheet(self):
        content_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
 xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
 <office:body><office:spreadsheet><table:table table:name="Sheet1">
  <table:table-row><table:table-cell><text:p>Date</text:p></table:table-cell>
   <table:table-cell><text:p>Value</text:p></table:table-cell></table:table-row>
  <table:table-row><table:table-cell><text:p>2026-01-01</text:p></table:table-cell>
   <table:table-cell office:value-type="float" office:value="42"/></table:table-row>
 </table:table></office:spreadsheet></office:body>
</office:document-content>"""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("content.xml", content_xml)

        headers, rows, truncated = parse_ods_data(buffer.getvalue(), max_rows=100)

        self.assertEqual(headers, ["Date", "Value"])
        self.assertEqual(rows, [["2026-01-01", "42"]])
        self.assertFalse(truncated)


class GristTableReadTests(unittest.TestCase):
    @patch("services.grist._read_json")
    def test_reads_the_first_data_table_as_rows(self, read_json):
        read_json.side_effect = [
            {"tables": [{"id": "GristHidden"}, {"id": "Sales"}]},
            {
                "records": [
                    {"id": 1, "fields": {"Date": "2026-01-01", "Revenue": 100}},
                    {"id": 2, "fields": {"Date": "2026-02-01", "Revenue": 125}},
                ]
            },
        ]

        headers, rows, table_id, truncated = read_grist_table(
            "http://grist:8484",
            "secret",
            document_id="doc-1",
        )

        self.assertEqual(headers, ["Date", "Revenue"])
        self.assertEqual(rows, [["2026-01-01", "100"], ["2026-02-01", "125"]])
        self.assertEqual(table_id, "Sales")
        self.assertFalse(truncated)


if __name__ == "__main__":
    unittest.main()
