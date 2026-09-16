import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from agent.base import DelegationContext
from agent.errors import PdfError
from agent.specialists.pdf import (
    PdfApplyTemplateAgent,
    PdfCreateAgent,
    PdfRunScriptAgent,
)


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
