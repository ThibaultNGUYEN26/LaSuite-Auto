"""Local-files capability block."""

from agent.blocks import (
    AgentBlock,
    ArtifactContract,
    CapabilityManifest,
    ConfigRequirement,
    WorkflowManifest,
)
from agent.specialists.local_files import (
    LocalFilesCreateFileAgent,
    LocalFilesListItemsAgent,
    LocalFilesReadImageAgent,
    LocalFilesReadPdfAgent,
)
from config import settings
from services.image import AlbertImageAnalyzer


def create_block() -> AgentBlock:
    image_analyzer = AlbertImageAnalyzer(
        settings.albert_api_key,
        base_url=settings.albert_base_url,
        requested_model=settings.albert_vision_model,
    )
    return AgentBlock(
        name="local_files",
        description="Read and create files below the configured local root.",
        required_config=(ConfigRequirement("LOCAL_FILES_ROOT", required=True),),
        permissions=("local.read", "local.write"),
        capabilities=(
            CapabilityManifest(
                "local_files_list_items",
                "List and locate files below the configured local root.",
                side_effect="local_read",
                permissions=("local.read",),
                produces=(ArtifactContract("file_reference"),),
            ),
            CapabilityManifest(
                "local_files_create_file",
                "Create a new text file below the configured local root.",
                side_effect="local_write",
                permissions=("local.write",),
                produces=(ArtifactContract("file"),),
            ),
            CapabilityManifest(
                "local_files_read_pdf",
                "Read selectable text from a local PDF.",
                side_effect="local_read",
                permissions=("local.read",),
                accepts=(ArtifactContract("file", ("application/pdf",)),),
                produces=(ArtifactContract("text", ("text/plain",)),),
            ),
            CapabilityManifest(
                "local_files_read_image",
                "Analyze a local image.",
                side_effect="local_read",
                permissions=("local.read", "model.vision"),
                accepts=(ArtifactContract("file", ("image/*",)),),
                produces=(ArtifactContract("image_analysis", ("text/plain",)),),
            ),
        ),
        workflows=(
            WorkflowManifest(
                "local_files.read_pdf",
                "Find a local PDF and read its content.",
                ("local_files_list_items", "local_files_read_pdf"),
            ),
        ),
        agents=(
            LocalFilesListItemsAgent(settings.local_files_root),
            LocalFilesCreateFileAgent(
                settings.local_files_root,
                max_create_bytes=settings.local_files_max_create_bytes,
            ),
            LocalFilesReadPdfAgent(
                settings.local_files_root,
                max_read_bytes=settings.local_files_max_read_bytes,
                max_text_characters=settings.pdf_max_text_characters,
            ),
            LocalFilesReadImageAgent(
                settings.local_files_root,
                image_analyzer,
                max_read_bytes=settings.image_max_read_bytes,
            ),
        ),
    )
