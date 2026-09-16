"""Run a bounded Python script for custom PDF edits the other tools cannot express."""

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import PdfError
from services.code_execution import MAX_TIMEOUT_SECONDS, run_python_code
from services.local_files import resolve_local_directory


class PdfRunScriptAgent(SpecialistAgent):
    name = "pdf_run_script"
    description = (
        "Run a short, bounded Python script for a custom PDF task that pdf_create "
        "and pdf_apply_template cannot express directly, such as merging PDFs, "
        "splitting or reordering pages, rotating pages, adding a watermark, filling "
        "form fields, or extracting embedded images. The script runs in this "
        "backend's own Python environment, where `pypdf` (reading and editing "
        "existing PDFs) and `fpdf` (fpdf2, building new PDFs from scratch) are "
        "already installed and ready to import - do not try to install packages. "
        "The script's working directory is the configured local workspace, so "
        "relative paths read and write files there. The script has no access to "
        "the conversation and must open any files it needs itself."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": (
                    "Python source code to execute. Import pypdf and/or fpdf as "
                    "needed and read/write files with paths relative to the local "
                    "workspace."
                ),
            },
            "timeout": {
                "type": "integer",
                "description": f"Maximum seconds to let the script run (1-{MAX_TIMEOUT_SECONDS}).",
                "default": 20,
            },
        },
        "required": ["code"],
        "additionalProperties": False,
    }

    def __init__(self, root: Path) -> None:
        self.root = root

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        code = arguments.get("code")
        if not isinstance(code, str):
            raise PdfError("code must be a string")
        timeout = arguments.get("timeout", 20)
        if not isinstance(timeout, int):
            raise PdfError("timeout must be an integer")
        working_directory = resolve_local_directory(self.root, ".")
        result = run_python_code(code, timeout=timeout, cwd=working_directory)
        return {"status": "executed", **result}
