"""Local-files specialist agents."""

from agent.specialists.local_files.create_file import LocalFilesCreateFileAgent
from agent.specialists.local_files.compare_pdfs import LocalFilesComparePdfsAgent
from agent.specialists.local_files.list_items import LocalFilesListItemsAgent
from agent.specialists.local_files.read_image import LocalFilesReadImageAgent
from agent.specialists.local_files.read_pdf import LocalFilesReadPdfAgent
from agent.specialists.local_files.read_text import LocalFilesReadTextAgent
from agent.specialists.local_files.rename_file import LocalFilesRenameFileAgent
from agent.specialists.local_files.search_pdfs import LocalFilesSearchPdfsAgent
from agent.specialists.local_files.search_pdf_memory import (
    LocalFilesSearchPdfMemoryAgent,
)
from agent.specialists.local_files.summarize_pdf import LocalFilesSummarizePdfAgent
from agent.specialists.local_files.summarize_pdfs import LocalFilesSummarizePdfsAgent

__all__ = [
    "LocalFilesCreateFileAgent",
    "LocalFilesComparePdfsAgent",
    "LocalFilesListItemsAgent",
    "LocalFilesReadImageAgent",
    "LocalFilesReadPdfAgent",
    "LocalFilesReadTextAgent",
    "LocalFilesRenameFileAgent",
    "LocalFilesSearchPdfsAgent",
    "LocalFilesSearchPdfMemoryAgent",
    "LocalFilesSummarizePdfAgent",
    "LocalFilesSummarizePdfsAgent",
]
