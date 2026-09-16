import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from agent.artifact_store import MemoryArtifactStore
from agent.base import DelegationContext
from agent.errors import PdfError
from agent.specialists.pdf import (
    PdfApplyTemplateAgent,
    PdfCreateAgent,
    PdfRenderAnalysisAgent,
    PdfRunScriptAgent,
)
from services.tabular_analysis import analyze_table


class PdfCreateAgentTests(unittest.TestCase):
    def test_creates_a_pdf_with_title_and_body(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agent = PdfCreateAgent(root)

            result = agent.execute(
                {
                    "directory": ".",
                    "file_name": "report",
                    "title": "Report",
                    "body_text": "Hello world.",
                },
                DelegationContext(conversation=()),
            )

            self.assertEqual(result["status"], "created")
            target = root / "report.pdf"
            self.assertTrue(target.exists())
            reader = PdfReader(str(target))
            self.assertEqual(len(reader.pages), 1)
            self.assertEqual(result["artifact"]["media_type"], "application/pdf")

    def test_never_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "report.pdf").write_bytes(b"%PDF-existing")
            agent = PdfCreateAgent(root)

            with self.assertRaisesRegex(PdfError, "already exists"):
                agent.execute(
                    {"directory": ".", "file_name": "report", "body_text": "x"},
                    DelegationContext(conversation=()),
                )

    def test_rejects_non_string_arguments(self):
        agent = PdfCreateAgent(Path("Documents"))

        with self.assertRaisesRegex(PdfError, "body_text must be a string"):
            agent.execute(
                {"directory": ".", "file_name": "report", "body_text": 5},
                DelegationContext(conversation=()),
            )


class PdfApplyTemplateAgentTests(unittest.TestCase):
    def test_compiles_a_typst_template(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes.typ").write_text(
                "= Title\n\nSome *bold* text.", encoding="utf-8"
            )
            agent = PdfApplyTemplateAgent(root)

            result = agent.execute(
                {
                    "source_relative_path": "notes.typ",
                    "directory": ".",
                    "file_name": "notes",
                },
                DelegationContext(conversation=()),
            )

            self.assertEqual(result["status"], "created")
            target = root / "notes.pdf"
            self.assertTrue(target.exists())

    def test_rejects_a_non_typst_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes.txt").write_text("hi", encoding="utf-8")
            agent = PdfApplyTemplateAgent(root)

            with self.assertRaisesRegex(PdfError, "\\.typ file"):
                agent.execute(
                    {
                        "source_relative_path": "notes.txt",
                        "directory": ".",
                        "file_name": "notes",
                    },
                    DelegationContext(conversation=()),
                )


class PdfRenderAnalysisAgentTests(unittest.TestCase):
    def test_renders_an_analysis_artifact_as_a_comprehensive_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = MemoryArtifactStore()
            analysis = analyze_table(
                ["date", "revenue", "region"],
                [
                    ["2026-01-01", "100", "North"],
                    ["2026-02-01", "130", "South"],
                    ["2026-03-01", "180", "North"],
                ],
                question="What is the revenue tendency?",
                requested_date_column="date",
                requested_value_columns=["revenue"],
            )
            artifact = store.put(
                {"analysis": analysis, "source_name": "sales.csv"},
                kind="data_analysis",
                media_type="application/vnd.lasuite.data-analysis+json",
                name="Sales analysis",
            )
            agent = PdfRenderAnalysisAgent(root, artifact_store=store)

            result = agent.execute(
                {
                    "artifact": artifact.tool_value(),
                    "directory": ".",
                    "file_name": "sales-report",
                    "title": "Sales report",
                },
                DelegationContext(conversation=()),
            )

            target = root / "sales-report.pdf"
            self.assertEqual(result["status"], "created")
            self.assertEqual(result["artifact"]["media_type"], "application/pdf")
            self.assertTrue(target.read_bytes().startswith(b"%PDF-"))
            extracted = "".join(
                page.extract_text() or "" for page in PdfReader(target).pages
            )
            self.assertIn("Executive summary", extracted)
            self.assertIn("Time-series analysis", extracted)
            self.assertIn("Methodology", extracted)

    def test_rejects_an_unknown_analysis_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            agent = PdfRenderAnalysisAgent(
                Path(directory), artifact_store=MemoryArtifactStore()
            )

            with self.assertRaisesRegex(PdfError, "no longer available"):
                agent.execute(
                    {
                        "artifact": {
                            "kind": "data_analysis",
                            "location": "memory",
                            "reference": "missing",
                            "media_type": "application/vnd.lasuite.data-analysis+json",
                            "metadata": {},
                        },
                        "directory": ".",
                        "file_name": "report",
                    },
                    DelegationContext(conversation=()),
                )


class PdfRunScriptAgentTests(unittest.TestCase):
    def test_runs_script_with_pdf_libraries_available_in_the_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agent = PdfRunScriptAgent(root)

            result = agent.execute(
                {
                    "code": (
                        "from fpdf import FPDF\n"
                        "import pypdf\n"
                        "pdf = FPDF()\n"
                        "pdf.add_page()\n"
                        "pdf.set_font('Helvetica', size=12)\n"
                        "pdf.cell(0, 10, 'hi')\n"
                        "pdf.output('script.pdf')\n"
                        "print('done')\n"
                    ),
                    "timeout": 15,
                },
                DelegationContext(conversation=()),
            )

            self.assertEqual(result["status"], "executed")
            self.assertEqual(result["exit_code"], 0)
            self.assertIn("done", result["stdout"])
            self.assertTrue((root / "script.pdf").exists())

    def test_rejects_non_string_code(self):
        agent = PdfRunScriptAgent(Path("Documents"))

        with self.assertRaisesRegex(PdfError, "code must be a string"):
            agent.execute(
                {"code": 5}, DelegationContext(conversation=())
            )


if __name__ == "__main__":
    unittest.main()
