"""La Suite Drive capability block."""

from agent.blocks import (
    AgentBlock,
    ArtifactContract,
    CapabilityManifest,
    ConfigRequirement,
    WorkflowManifest,
)
from agent.specialists.drive import (
    DriveConfigAgent,
    DriveCreateFileAgent,
    DriveListItemsAgent,
    DriveReadImageAgent,
    DriveReadPdfAgent,
    DriveUploadFileAgent,
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
        name="drive",
        description="Read and write files in La Suite Drive.",
        required_config=(
            ConfigRequirement("DRIVE_BASE_URL", required=True),
            ConfigRequirement("DRIVE_SESSION_ID", required=True, secret=True),
            ConfigRequirement("DRIVE_CSRF_TOKEN", secret=True),
        ),
        permissions=("drive.read", "drive.write", "local.read"),
        capabilities=(
            CapabilityManifest(
                "drive_get_config",
                "Read public Drive instance configuration.",
                side_effect="external_read",
                permissions=("drive.read",),
            ),
            CapabilityManifest(
                "drive_create_file",
                "Create a text file in Drive.",
                side_effect="external_write",
                permissions=("drive.write",),
                produces=(ArtifactContract("file", description="Drive file"),),
            ),
            CapabilityManifest(
                "drive_list_items",
                "List and locate Drive items.",
                side_effect="external_read",
                permissions=("drive.read",),
                produces=(ArtifactContract("file_reference"),),
            ),
            CapabilityManifest(
                "drive_read_pdf",
                "Read selectable text from a Drive PDF.",
                side_effect="external_read",
                permissions=("drive.read",),
                accepts=(ArtifactContract("file", ("application/pdf",)),),
                produces=(ArtifactContract("text", ("text/plain",)),),
            ),
            CapabilityManifest(
                "drive_read_image",
                "Analyze an image stored in Drive.",
                side_effect="external_read",
                permissions=("drive.read", "model.vision"),
                accepts=(ArtifactContract("file", ("image/*",)),),
                produces=(ArtifactContract("image_analysis", ("text/plain",)),),
            ),
            CapabilityManifest(
                "drive_upload_file",
                "Upload an existing file to Drive without changing its bytes.",
                side_effect="external_write",
                permissions=("local.read", "drive.write"),
                accepts=(ArtifactContract("file"),),
                produces=(ArtifactContract("file"),),
            ),
        ),
        workflows=(
            WorkflowManifest(
                "drive.read_pdf",
                "Find a PDF in Drive and read its content.",
                ("drive_list_items", "drive_read_pdf"),
            ),
        ),
        agents=(
            DriveConfigAgent(settings.drive_base_url),
            DriveCreateFileAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                csrf_token=settings.drive_csrf_token,
                upload_acl=settings.drive_upload_acl,
                max_create_bytes=settings.drive_max_create_bytes,
            ),
            DriveListItemsAgent(
                settings.drive_base_url,
                settings.drive_session_id,
            ),
            DriveReadPdfAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                max_download_bytes=settings.drive_max_download_bytes,
                max_text_characters=settings.pdf_max_text_characters,
            ),
            DriveReadImageAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                image_analyzer,
                max_download_bytes=settings.image_max_read_bytes,
            ),
            DriveUploadFileAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                settings.local_files_root,
                csrf_token=settings.drive_csrf_token,
                upload_acl=settings.drive_upload_acl,
                max_upload_bytes=settings.drive_max_upload_bytes,
            ),
        ),
    )
