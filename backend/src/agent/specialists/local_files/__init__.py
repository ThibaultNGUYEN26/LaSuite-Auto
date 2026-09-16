"""Local-files specialist agents."""

from agent.specialists.local_files.create_file import LocalFilesCreateFileAgent
from agent.specialists.local_files.list_items import LocalFilesListItemsAgent
from agent.specialists.local_files.read_image import LocalFilesReadImageAgent
from agent.specialists.local_files.read_pdf import LocalFilesReadPdfAgent
from agent.specialists.local_files.read_text import LocalFilesReadTextAgent
from agent.specialists.local_files.rename_file import LocalFilesRenameFileAgent

__all__ = [
    "LocalFilesCreateFileAgent",
    "LocalFilesListItemsAgent",
    "LocalFilesReadImageAgent",
    "LocalFilesReadPdfAgent",
    "LocalFilesReadTextAgent",
    "LocalFilesRenameFileAgent",
]
