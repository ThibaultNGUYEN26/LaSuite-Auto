"""Local-files capability block."""

from agent.blocks import (
    AgentBlock,
    ArtifactContract,
    CapabilityManifest,
    ConfigRequirement,
    WorkflowManifest,
)
from agent.specialists.local_files import (
    LocalFilesAnalyzeFolderAgent,
    LocalFilesAuditFolderAgent,
    LocalFilesAuditPdfAgent,
    LocalFilesComparePdfsAgent,
    LocalFilesCreateFileAgent,
    LocalFilesCreateFolderAgent,
    LocalFilesListItemsAgent,
    LocalFilesReadImageAgent,
    LocalFilesReadPdfAgent,
    LocalFilesReadTextAgent,
    LocalFilesRenameFileAgent,
    LocalFilesSearchPdfsAgent,
    LocalFilesSearchPdfMemoryAgent,
    LocalFilesSummarizePdfAgent,
    LocalFilesSummarizePdfsAgent,
)
from config import settings
from services.image import AlbertImageAnalyzer


def create_block() -> AgentBlock:
    image_analyzer = AlbertImageAnalyzer(
        settings.albert_api_key,
        base_url=settings.albert_base_url,
        requested_model=settings.albert_vision_model,
    )
    pdf_summarizer = LocalFilesSummarizePdfAgent(
        settings.local_files_root,
        api_key=settings.albert_api_key,
        base_url=settings.albert_base_url,
        requested_model=settings.albert_model,
        max_read_bytes=settings.local_files_max_read_bytes,
        max_pages=settings.pdf_search_max_pages,
    )
    pdf_batch_summarizer = LocalFilesSummarizePdfsAgent(
        settings.local_files_root,
        pdf_summarizer,
        max_files=settings.pdf_memory_max_batch_files,
        concurrency=settings.pdf_memory_batch_concurrency,
    )
    return AgentBlock(
        name="local_files",
        description=(
            "Discover, search, read, create, and rename files below the configured "
            "local root. It can privately prepare complete PDFs for analysis, review, "
            "auditing, and later questions without requiring users to request an "
            "intermediate file. Search page-level evidence across a folder of PDFs, "
            "or locate an existing dataset before another block analyzes it."
        ),
        required_config=(ConfigRequirement("LOCAL_FILES_ROOT", required=True),),
        permissions=("local.read", "local.write"),
        capabilities=(
            CapabilityManifest(
                "local_files_list_items",
                "Search and list files inside the local root or a selected folder.",
                side_effect="local_read",
                permissions=("local.read",),
                accepts=(ArtifactContract("folder"),),
                produces=(ArtifactContract("file_reference"),),
            ),
            CapabilityManifest(
                "local_files_create_folder",
                "Create a new local folder and return its reusable relative path.",
                side_effect="local_write",
                permissions=("local.write",),
                accepts=(ArtifactContract("folder"),),
                produces=(ArtifactContract("folder", ("inode/directory",)),),
            ),
            CapabilityManifest(
                "local_files_create_file",
                "Create a new text file below the configured local root.",
                side_effect="local_write",
                permissions=("local.write",),
                produces=(ArtifactContract("file"),),
            ),
            CapabilityManifest(
                "local_files_rename_file",
                "Rename a local file in its current directory without overwriting.",
                side_effect="local_write",
                permissions=("local.read", "local.write"),
                accepts=(ArtifactContract("file"),),
                produces=(ArtifactContract("file"),),
            ),
            CapabilityManifest(
                "local_files_read_pdf",
                "Read page-labelled text from a local PDF for grounded analysis and follow-up questions.",
                side_effect="local_read",
                permissions=("local.read",),
                accepts=(ArtifactContract("file", ("application/pdf",)),),
                produces=(ArtifactContract("text", ("text/plain",)),),
            ),
            CapabilityManifest(
                "local_files_search_pdfs",
                "Search relevant pages across many local PDFs and return cited evidence.",
                side_effect="local_read",
                permissions=("local.read",),
                produces=(ArtifactContract("document_matches", ("text/plain",)),),
            ),
            CapabilityManifest(
                "local_files_summarize_pdf",
                "Privately prepare and analyze every page of one local PDF for immediate and later use.",
                side_effect="local_write",
                permissions=("local.read", "local.write", "model.generate"),
                accepts=(ArtifactContract("file", ("application/pdf",)),),
                produces=(ArtifactContract("file", ("text/markdown",)),),
                internal=True,
            ),
            CapabilityManifest(
                "local_files_summarize_pdfs",
                "Privately prepare PDFs from one or several folders in a bounded batch.",
                side_effect="local_write",
                permissions=("local.read", "local.write", "model.generate"),
                accepts=(ArtifactContract("file", ("application/pdf",)),),
                produces=(ArtifactContract("file", ("text/markdown",)),),
                internal=True,
            ),
            CapabilityManifest(
                "local_files_analyze_folder",
                "Descriptively analyze every PDF, CSV, and text document in one folder, create reusable PDF memories, and keep each document summary separate without auditing or comparing.",
                side_effect="local_write",
                permissions=("local.read", "local.write", "model.generate"),
                accepts=(
                    ArtifactContract("folder", ("inode/directory",)),
                    ArtifactContract("file", ("application/pdf", "text/*")),
                ),
                produces=(ArtifactContract("document_analysis", ("text/markdown",)),),
            ),
            CapabilityManifest(
                "local_files_compare_pdfs",
                "Compare two local PDFs using both reusable memories and original-page evidence.",
                side_effect="local_write",
                permissions=("local.read", "local.write", "model.generate"),
                accepts=(ArtifactContract("file", ("application/pdf",)),),
                produces=(ArtifactContract("comparison", ("text/markdown",)),),
            ),
            CapabilityManifest(
                "local_files_audit_pdf",
                "Audit a client represented by exactly one PDF against one reference PDF.",
                side_effect="local_write",
                permissions=("local.read", "local.write", "model.generate"),
                accepts=(ArtifactContract("file", ("application/pdf",)),),
                produces=(ArtifactContract("audit", ("text/markdown",)),),
            ),
            CapabilityManifest(
                "local_files_audit_folder",
                "Audit every PDF, CSV, and text evidence file in one client folder against a reference PDF, with one finding per criterion and a reusable source register for reopening cited evidence.",
                side_effect="local_write",
                permissions=("local.read", "local.write", "model.generate"),
                accepts=(
                    ArtifactContract("folder", ("inode/directory",)),
                    ArtifactContract("file", ("application/pdf",)),
                ),
                produces=(
                    ArtifactContract(
                        "audit_report",
                        ("application/vnd.lasuite.audit+json",),
                    ),
                    ArtifactContract("file", ("application/pdf", "text/*", "text/csv")),
                ),
            ),
            CapabilityManifest(
                "local_files_search_pdf_memory",
                "Search saved PDF memories to identify original PDFs for a question.",
                side_effect="local_read",
                permissions=("local.read",),
                produces=(ArtifactContract("document_matches", ("text/markdown",)),),
            ),
            CapabilityManifest(
                "local_files_read_text",
                "Read CSV and other text-based local files.",
                side_effect="local_read",
                permissions=("local.read",),
                accepts=(ArtifactContract("file", ("text/*", "application/json")),),
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
                "Find a local PDF and read page-labelled content for grounded answers.",
                ("local_files_list_items", "local_files_read_pdf"),
            ),
            WorkflowManifest(
                "local_files.create_folder_and_file",
                "Create a folder, then create a text file inside its returned path.",
                ("local_files_create_folder", "local_files_create_file"),
            ),
            WorkflowManifest(
                "local_files.answer_from_pdfs",
                "Use saved memories to identify PDFs, then answer from cited page evidence.",
                ("local_files_search_pdf_memory", "local_files_search_pdfs"),
            ),
            WorkflowManifest(
                "local_files.remember_pdf",
                "Analyze an entire local PDF and create a reusable Markdown memory.",
                ("local_files_list_items", "local_files_summarize_pdf"),
            ),
            WorkflowManifest(
                "local_files.analyze_pdf",
                "Analyze or review an entire PDF while privately preparing it for future questions.",
                ("local_files_list_items", "local_files_summarize_pdf"),
            ),
            WorkflowManifest(
                "local_files.analyze_folder",
                "Analyze all documents in one selected folder in a single bounded operation without performing an audit.",
                ("local_files_list_items", "local_files_analyze_folder"),
            ),
            WorkflowManifest(
                "local_files.remember_pdfs",
                "Create independent reusable memories for a folder or list of PDFs.",
                ("local_files_summarize_pdfs",),
            ),
            WorkflowManifest(
                "local_files.compare_pdfs",
                "Compare two PDFs from their full-document memories and cited original pages.",
                ("local_files_compare_pdfs",),
            ),
            WorkflowManifest(
                "local_files.audit_pdf",
                "Audit one client PDF against a reference checklist with original-page evidence.",
                ("local_files_list_items", "local_files_audit_pdf"),
            ),
            WorkflowManifest(
                "local_files.audit_folder",
                "Audit a complete client folder against a reference checklist in one bounded operation.",
                ("local_files_list_items", "local_files_audit_folder"),
            ),
        ),
        agents=(
            LocalFilesListItemsAgent(settings.local_files_root),
            LocalFilesCreateFolderAgent(settings.local_files_root),
            LocalFilesCreateFileAgent(
                settings.local_files_root,
                max_create_bytes=settings.local_files_max_create_bytes,
            ),
            LocalFilesRenameFileAgent(settings.local_files_root),
            LocalFilesReadPdfAgent(
                settings.local_files_root,
                max_read_bytes=settings.local_files_max_read_bytes,
                max_text_characters=settings.pdf_max_text_characters,
            ),
            LocalFilesSearchPdfsAgent(
                settings.local_files_root,
                max_read_bytes=settings.local_files_max_read_bytes,
                max_files=settings.pdf_search_max_local_files,
                max_total_pages=settings.pdf_search_max_pages,
            ),
            pdf_summarizer,
            pdf_batch_summarizer,
            LocalFilesAnalyzeFolderAgent(
                settings.local_files_root,
                pdf_batch_summarizer,
                api_key=settings.albert_api_key,
                base_url=settings.albert_base_url,
                requested_model=settings.albert_model,
                max_read_bytes=settings.local_files_max_read_bytes,
                max_text_characters=settings.text_max_characters,
                max_files=settings.pdf_search_max_local_files,
            ),
            LocalFilesComparePdfsAgent(
                settings.local_files_root,
                pdf_summarizer,
                api_key=settings.albert_api_key,
                base_url=settings.albert_base_url,
                requested_model=settings.albert_model,
                max_read_bytes=settings.local_files_max_read_bytes,
                max_total_pages=settings.pdf_search_max_pages,
            ),
            LocalFilesAuditPdfAgent(
                settings.local_files_root,
                pdf_summarizer,
                api_key=settings.albert_api_key,
                base_url=settings.albert_base_url,
                requested_model=settings.albert_model,
                max_read_bytes=settings.local_files_max_read_bytes,
                max_total_pages=settings.pdf_search_max_pages,
            ),
            LocalFilesAuditFolderAgent(
                settings.local_files_root,
                pdf_summarizer,
                api_key=settings.albert_api_key,
                base_url=settings.albert_base_url,
                requested_model=settings.albert_model,
                max_read_bytes=settings.local_files_max_read_bytes,
                max_text_characters=settings.text_max_characters,
                max_files=settings.pdf_search_max_local_files,
                max_total_pages=settings.pdf_search_max_pages,
                max_create_bytes=settings.local_files_max_create_bytes,
                batch_summarizer=pdf_batch_summarizer,
                backend_url=settings.backend_url,
            ),
            LocalFilesSearchPdfMemoryAgent(settings.local_files_root),
            LocalFilesReadTextAgent(
                settings.local_files_root,
                max_read_bytes=settings.local_files_max_read_bytes,
                max_text_characters=settings.text_max_characters,
            ),
            LocalFilesReadImageAgent(
                settings.local_files_root,
                image_analyzer,
                max_read_bytes=settings.image_max_read_bytes,
            ),
        ),
    )
