"""Data-analysis capability block."""

from agent.blocks import (
    AgentBlock,
    ArtifactContract,
    CapabilityManifest,
    ConfigRequirement,
    WorkflowManifest,
)
from agent.specialists.data_analysis import AnalyzeTableAgent
from config import settings


def create_block() -> AgentBlock:
    return AgentBlock(
        name="data_analysis",
        description=(
            "Analyze CSV, OpenDocument spreadsheet, and Grist tabular data; "
            "answer questions about statistics, tendencies, evolution, comparisons, "
            "and change over time; produce typed analysis artifacts that the PDF "
            "block can render as reports."
        ),
        required_config=(
            ConfigRequirement("LOCAL_FILES_ROOT", required=True),
            ConfigRequirement("DRIVE_BASE_URL"),
            ConfigRequirement("DRIVE_SESSION_ID", secret=True),
            ConfigRequirement("GRIST_BASE_URL"),
            ConfigRequirement("GRIST_API_KEY", secret=True),
        ),
        permissions=("local.read", "drive.read", "grist.read"),
        capabilities=(
            CapabilityManifest(
                "data_analyze_table",
                "Analyze tabular data and produce a reusable analysis artifact.",
                side_effect="local_read",
                permissions=(
                    "local.read",
                    "drive.read",
                    "grist.read",
                ),
                accepts=(
                    ArtifactContract(
                        "file",
                        (
                            "text/csv",
                            "application/vnd.oasis.opendocument.spreadsheet",
                        ),
                    ),
                    ArtifactContract("grist_document"),
                ),
                produces=(ArtifactContract(
                    "data_analysis",
                    ("application/vnd.lasuite.data-analysis+json",),
                ),),
            ),
        ),
        workflows=(
            WorkflowManifest(
                "data_analysis.create_pdf_report",
                "Analyze tabular data and render the result as a comprehensive PDF.",
                ("data_analyze_table", "pdf_render_analysis"),
            ),
            WorkflowManifest(
                "data_analysis.publish_report",
                "Analyze tabular data, render a PDF report, and publish it to Drive.",
                ("data_analyze_table", "pdf_render_analysis", "drive_upload_file"),
            ),
        ),
        agents=(
            AnalyzeTableAgent(
                local_files_root=settings.local_files_root,
                drive_base_url=settings.drive_base_url,
                drive_session_id=settings.drive_session_id,
                grist_base_url=settings.grist_base_url,
                grist_api_key=settings.grist_api_key,
                max_source_bytes=settings.data_analysis_max_source_bytes,
                max_rows=settings.data_analysis_max_rows,
            ),
        ),
    )
