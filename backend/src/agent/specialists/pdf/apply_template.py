"""Compile a local Typst template file into a PDF."""

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import PdfError
from services.local_files import resolve_local_file
from services.pdf import render_typst_template_to_local_pdf


class PdfApplyTemplateAgent(SpecialistAgent):
    name = "pdf_apply_template"
    description = (
        "Compile a local Typst (.typ) template file into a PDF. Use this for "
        "structured or repeated documents - reports, letters, invoices - where "
        "the layout (headers, footers, page numbers, styling) is authored "
        "directly in the template using Typst markup and #set page(...) rules. "
        "The source file must already exist below the local workspace; find it "
        "with local_files_list_items first."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "source_relative_path": {
                "type": "string",
                "description": (
                    "Path to the source .typ Typst template, relative to the "
                    "local workspace, exactly as returned by local_files_list_items."
                ),
            },
            "directory": {
                "type": "string",
                "description": (
                    "Existing destination directory for the generated PDF, "
                    "relative to the local workspace. Use . for the workspace root."
                ),
            },
            "file_name": {
                "type": "string",
                "description": "File name for the generated PDF, without extension.",
            },
        },
        "required": ["source_relative_path", "directory", "file_name"],
        "additionalProperties": False,
    }

    def __init__(self, root: Path, *, max_source_bytes: int = 5 * 1024 * 1024) -> None:
        self.root = root
        self.max_source_bytes = max_source_bytes

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        for key in ("source_relative_path", "directory", "file_name"):
            if not isinstance(arguments.get(key), str):
                raise PdfError(f"{key} must be a string")

        source_relative_path = arguments["source_relative_path"]
        if not source_relative_path.lower().endswith(".typ"):
            raise PdfError("source_relative_path must point to a .typ file")
        source_path = resolve_local_file(self.root, source_relative_path)
        if source_path.stat().st_size > self.max_source_bytes:
            raise PdfError(
                f"Typst template exceeds the configured {self.max_source_bytes}-byte limit"
            )

        return render_typst_template_to_local_pdf(
            self.root,
            source_path=source_path,
            directory=arguments["directory"],
            file_name=arguments["file_name"],
        )
