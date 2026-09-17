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
    PdfRenderAnalysisAgent,
    PdfRenderAuditAgent,
    PdfRunScriptAgent,
)
from config import settings


def create_block() -> AgentBlock:
    return AgentBlock(
        name="pdf",
        description=(
            "Create, template, and script custom edits to PDF documents in the "
            "local workspace, and render comprehensive reports from structured "
            "data-analysis or audit-report artifacts without copying large report "
            "bodies through the coordinator."
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
                "pdf_render_analysis",
                "Render a data-analysis artifact as a comprehensive PDF report.",
                side_effect="local_write",
                permissions=("local.write",),
                accepts=(ArtifactContract(
                    "data_analysis",
                    ("application/vnd.lasuite.data-analysis+json",),
                ),),
                produces=(ArtifactContract("file", ("application/pdf",)),),
                confirmation_required=True,
            ),
            CapabilityManifest(
                "pdf_render_audit",
                "Render a complete audit-report artifact as a local PDF without copying its full contents through the model context.",
                side_effect="local_write",
                permissions=("local.write",),
                accepts=(ArtifactContract(
                    "audit_report",
                    ("application/vnd.lasuite.audit+json",),
                ),),
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
            PdfRenderAnalysisAgent(
                settings.local_files_root,
                max_report_bytes=settings.pdf_max_report_bytes,
            ),
            PdfRenderAuditAgent(
                settings.local_files_root,
                max_report_bytes=settings.pdf_max_report_bytes,
            ),
            PdfRunScriptAgent(settings.local_files_root),
        ),
    )
