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
    DriveCreateFilesAgent,
    DriveDownloadFolderAgent,
    DriveListItemsAgent,
    DriveReadImageAgent,
    DriveReadPdfAgent,
    DriveReadTextAgent,
    DriveRenameFileAgent,
    DriveSearchPdfsAgent,
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
        description=(
            "Discover, search, read, create, upload, rename, and download files or "
            "complete folder trees in La Suite Drive, including page-level evidence "
            "search across many PDFs."
        ),
        required_config=(
            ConfigRequirement("DRIVE_BASE_URL", required=True),
            ConfigRequirement("DRIVE_SESSION_ID", required=True, secret=True),
            ConfigRequirement("DRIVE_CSRF_TOKEN", secret=True),
        ),
        permissions=("drive.read", "drive.write", "local.read", "local.write"),
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
                "drive_create_files",
                "Create multiple text files in Drive in one bounded batch.",
                side_effect="external_write",
                permissions=("drive.write",),
                produces=(ArtifactContract("file", description="Drive files"),),
            ),
            CapabilityManifest(
                "drive_list_items",
                "List and locate Drive items.",
                side_effect="external_read",
                permissions=("drive.read",),
                produces=(ArtifactContract("file_reference"),),
            ),
            CapabilityManifest(
                "drive_download_folder",
                "Download all My Files or a bounded Drive folder tree locally while preserving paths and bytes.",
                side_effect="local_write",
                permissions=("drive.read", "local.write"),
                accepts=(ArtifactContract("folder", ("inode/directory",)),),
                produces=(ArtifactContract("folder", ("inode/directory",)),),
            ),
            CapabilityManifest(
                "drive_read_pdf",
                "Read page-labelled text from a Drive PDF for grounded analysis and follow-up questions.",
                side_effect="external_read",
                permissions=("drive.read",),
                accepts=(ArtifactContract("file", ("application/pdf",)),),
                produces=(ArtifactContract("text", ("text/plain",)),),
            ),
            CapabilityManifest(
                "drive_search_pdfs",
                "Search relevant pages across many Drive PDFs and return cited evidence.",
                side_effect="external_read",
                permissions=("drive.read",),
                produces=(ArtifactContract("document_matches", ("text/plain",)),),
            ),
            CapabilityManifest(
                "drive_read_text",
                "Read CSV and other text-based Drive files.",
                side_effect="external_read",
                permissions=("drive.read",),
                accepts=(ArtifactContract("file", ("text/*", "application/json")),),
                produces=(ArtifactContract("text", ("text/plain",)),),
            ),
            CapabilityManifest(
                "drive_rename_file",
                "Rename a Drive file without changing its contents.",
                side_effect="external_write",
                permissions=("drive.read", "drive.write"),
                accepts=(ArtifactContract("file"),),
                produces=(ArtifactContract("file"),),
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
                "Find a PDF in Drive and read page-labelled content for grounded answers.",
                ("drive_list_items", "drive_read_pdf"),
            ),
            WorkflowManifest(
                "drive.download_folder",
                "Locate a Drive folder and download its complete bounded tree locally.",
                ("drive_list_items", "drive_download_folder"),
            ),
            WorkflowManifest(
                "drive.answer_from_pdfs",
                "Search a Drive PDF collection and answer from cited page evidence.",
                ("drive_search_pdfs",),
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
            DriveCreateFilesAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                csrf_token=settings.drive_csrf_token,
                upload_acl=settings.drive_upload_acl,
                max_create_bytes=settings.drive_max_create_bytes,
                max_batch_files=settings.drive_max_batch_files,
            ),
            DriveListItemsAgent(
                settings.drive_base_url,
                settings.drive_session_id,
            ),
            DriveDownloadFolderAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                settings.local_files_root,
                max_file_bytes=settings.drive_max_download_bytes,
                max_files=settings.drive_max_folder_download_files,
                max_total_bytes=settings.drive_max_folder_download_bytes,
            ),
            DriveReadPdfAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                max_download_bytes=settings.drive_max_download_bytes,
                max_text_characters=settings.pdf_max_text_characters,
            ),
            DriveSearchPdfsAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                max_download_bytes=settings.drive_max_download_bytes,
                max_files=settings.pdf_search_max_drive_files,
                max_total_pages=settings.pdf_search_max_pages,
            ),
            DriveReadTextAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                max_download_bytes=settings.drive_max_download_bytes,
                max_text_characters=settings.text_max_characters,
            ),
            DriveRenameFileAgent(
                settings.drive_base_url,
                settings.drive_session_id,
                csrf_token=settings.drive_csrf_token,
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
