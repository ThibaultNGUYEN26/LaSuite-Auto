"""PDF capability block."""

from agent.blocks import (
    AgentBlock,
    ArtifactContract,
    CapabilityManifest,
    ConfigRequirement,
)
from agent.specialists.pdf import (
    PdfApplyTemplateAgent,
    PdfCreateAgent,
    PdfRunScriptAgent,
)
from config import settings


def create_block() -> AgentBlock:
    return AgentBlock(
        name="pdf",
        description=(
            "Create, template, and script custom edits to PDF documents in the "
            "local workspace."
        ),
        required_config=(ConfigRequirement("LOCAL_FILES_ROOT", required=True),),
        permissions=("local.read", "local.write", "process.execute"),
        capabilities=(
            CapabilityManifest(
                "pdf_create",
                "Create a simple PDF from a title and plain-text body.",
                side_effect="local_write",
                permissions=("local.write",),
                produces=(ArtifactContract("file", ("application/pdf",)),),
                confirmation_required=True,
            ),
            CapabilityManifest(
                "pdf_apply_template",
                "Compile a local Typst (.typ) template file into a PDF.",
                side_effect="local_write",
                permissions=("local.read", "local.write"),
                accepts=(ArtifactContract("file", ("text/x-typst",)),),
                produces=(ArtifactContract("file", ("application/pdf",)),),
                confirmation_required=True,
            ),
            CapabilityManifest(
                "pdf_run_script",
                (
                    "Run a bounded Python script, with pypdf and fpdf already "
                    "installed, for custom PDF edits."
                ),
                side_effect="code_execution",
                permissions=("local.read", "local.write", "process.execute"),
                confirmation_required=True,
            ),
        ),
        agents=(
            PdfCreateAgent(
                settings.local_files_root,
                max_body_characters=settings.pdf_max_create_characters,
            ),
            PdfApplyTemplateAgent(
                settings.local_files_root,
                max_source_bytes=settings.pdf_max_template_source_bytes,
            ),
            PdfRunScriptAgent(settings.local_files_root),
        ),
    )
