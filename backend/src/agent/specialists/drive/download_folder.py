"""Download a Drive folder tree to the configured local workspace."""

from __future__ import annotations

import asyncio
import io
from pathlib import Path
from pathlib import PurePosixPath
import stat
from typing import Any
from zipfile import BadZipFile, ZipFile

from agent.artifacts import Artifact
from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError, LocalFilesError
from services.drive import (
    download_drive_file,
    download_drive_folder_archive,
    get_drive_item,
    list_drive_items,
)
from services.local_files import (
    WINDOWS_RESERVED_NAMES,
    create_local_directory,
    resolve_local_directory,
)


def _safe_component(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise DriveAPIError(f"{field} is missing")
    clean = value.strip()
    if (
        not clean
        or clean in {".", ".."}
        or Path(clean).name != clean
        or any(character in clean for character in '<>:"/\\|?*')
        or clean.endswith((" ", "."))
        or Path(clean).stem.upper() in WINDOWS_RESERVED_NAMES
    ):
        raise DriveAPIError(f"{field} contains characters unsafe for a local path")
    return clean


def _extract_folder_archive(
    archive_data: bytes,
    *,
    destination_root: Path,
    local_files_root: Path,
    max_file_bytes: int,
    max_files: int,
    max_total_bytes: int,
) -> dict[str, Any]:
    """Safely extract a Drive ZIP with bounded files and no path traversal."""
    downloaded = 0
    failed = 0
    skipped = 0
    total_bytes = 0
    results: list[dict[str, Any]] = []
    file_limit_reached = False
    try:
        archive = ZipFile(io.BytesIO(archive_data))
    except BadZipFile as exc:
        raise DriveAPIError("Drive returned an invalid ZIP folder archive") from exc

    with archive:
        for member in archive.infolist():
            raw_name = member.filename.replace("\\", "/")
            path = PurePosixPath(raw_name)
            try:
                if path.is_absolute() or not path.parts or ".." in path.parts:
                    raise DriveAPIError("ZIP entry has an unsafe path")
                parts = [
                    _safe_component(part, field="ZIP entry name")
                    for part in path.parts
                    if part not in {"", "."}
                ]
                if not parts:
                    continue
                mode = member.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise DriveAPIError("ZIP symbolic links are not allowed")
                target = destination_root.joinpath(*parts).resolve()
                target.relative_to(destination_root)
                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if downloaded + skipped >= max_files:
                    file_limit_reached = True
                    skipped += 1
                    results.append(
                        {"status": "skipped", "name": raw_name, "reason": "file_limit"}
                    )
                    continue
                if member.file_size > max_file_bytes:
                    skipped += 1
                    results.append(
                        {"status": "skipped", "name": raw_name, "reason": "file_too_large"}
                    )
                    continue
                if member.file_size > max_total_bytes - total_bytes:
                    skipped += 1
                    results.append(
                        {"status": "skipped", "name": raw_name, "reason": "total_size_limit"}
                    )
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                data = archive.read(member)
                with target.open("xb") as output:
                    output.write(data)
                total_bytes += len(data)
                downloaded += 1
                results.append(
                    {
                        "status": "downloaded",
                        "relative_path": target.relative_to(
                            local_files_root.expanduser().resolve()
                        ).as_posix(),
                        "bytes_written": len(data),
                    }
                )
            except (DriveAPIError, OSError, ValueError, RuntimeError, BadZipFile) as exc:
                failed += 1
                results.append(
                    {"status": "failed", "name": raw_name, "error": str(exc)}
                )
    return {
        "downloaded": downloaded,
        "failed": failed,
        "skipped": skipped,
        "bytes_written": total_bytes,
        "limited": file_limit_reached or skipped > 0,
        "results": results,
    }


class DriveDownloadFolderAgent(SpecialistAgent):
    name = "drive_download_folder"
    description = (
        "Download the entire La Suite Drive My Files area or one selected Drive folder "
        "to the local workspace while preserving nested folders and original file "
        "bytes. Use when the user asks to download, copy, export, or back up Drive "
        "content. For a selected folder, first locate its UUID with drive_list_items; "
        "omit folder_id for all of My Files. Call this once rather than downloading "
        "files one by one. It never overwrites an existing local folder or file and "
        "reports partial failures and configured limits."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "folder_id": {
                "type": "string",
                "format": "uuid",
                "description": (
                    "Optional Drive folder UUID returned by drive_list_items. Omit "
                    "to download the complete My Files area."
                ),
            },
            "local_directory": {
                "type": "string",
                "description": (
                    "Existing destination below LOCAL_FILES_ROOT, such as Downloads. "
                    "The downloaded folder is created inside it."
                ),
            },
            "destination_name": {
                "type": "string",
                "description": (
                    "Optional local folder name. Defaults to the Drive folder title."
                ),
            },
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "description": "Maximum nested Drive depth. Defaults to 5.",
            },
        },
        "required": ["local_directory"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        base_url: str,
        session_id: str | None,
        local_files_root: Path,
        *,
        max_file_bytes: int,
        max_files: int,
        max_total_bytes: int,
    ) -> None:
        if max_file_bytes < 1 or max_files < 1 or max_total_bytes < 1:
            raise ValueError("Drive folder download limits must be positive")
        self.base_url = base_url
        self.session_id = session_id or ""
        self.local_files_root = local_files_root
        self.max_file_bytes = max_file_bytes
        self.max_files = max_files
        self.max_total_bytes = max_total_bytes

    async def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        folder_id = arguments.get("folder_id")
        local_directory = arguments.get("local_directory")
        destination_name = arguments.get("destination_name")
        max_depth = arguments.get("max_depth", 5)
        if folder_id is not None and not isinstance(folder_id, str):
            raise DriveAPIError("folder_id must be a string")
        if not isinstance(local_directory, str):
            raise LocalFilesError("local_directory must be a string")
        if destination_name is not None and not isinstance(destination_name, str):
            raise LocalFilesError("destination_name must be a string")
        if not isinstance(max_depth, int) or isinstance(max_depth, bool):
            raise DriveAPIError("max_depth must be an integer")

        if folder_id is not None:
            item = await asyncio.to_thread(
                get_drive_item, self.base_url, self.session_id, folder_id
            )
            if item.get("type") != "folder":
                raise DriveAPIError("The selected Drive item is not a folder")
            default_name = item.get("title")
        else:
            default_name = "My Drive"
        root_name = _safe_component(
            destination_name if destination_name is not None else default_name,
            field="destination folder name",
        )
        destination_parent = resolve_local_directory(
            self.local_files_root, local_directory
        )
        if (destination_parent / root_name).exists():
            raise LocalFilesError(
                "A file or folder with this name already exists"
            )
        if folder_id is not None:
            archive_data = await asyncio.to_thread(
                download_drive_folder_archive,
                self.base_url,
                self.session_id,
                folder_id,
                max_bytes=self.max_total_bytes,
            )
            created = create_local_directory(
                self.local_files_root,
                parent_directory=local_directory,
                folder_name=root_name,
            )
            destination_root = resolve_local_directory(
                self.local_files_root, created["relative_path"]
            )
            extracted = await asyncio.to_thread(
                _extract_folder_archive,
                archive_data,
                destination_root=destination_root,
                local_files_root=self.local_files_root,
                max_file_bytes=self.max_file_bytes,
                max_files=self.max_files,
                max_total_bytes=self.max_total_bytes,
            )
            complete = not extracted["limited"] and extracted["failed"] == 0
            return {
                "status": "downloaded" if complete else "partially_downloaded",
                "drive_folder_id": folder_id,
                "destination_relative_path": created["relative_path"],
                **extracted,
                "complete": complete,
                "source_limitation": None,
                "artifact": Artifact(
                    kind="folder",
                    location="local",
                    reference=created["relative_path"],
                    media_type="inode/directory",
                    name=root_name,
                ).tool_value(),
            }
        listing = await asyncio.to_thread(
            list_drive_items,
            self.base_url,
            self.session_id,
            limit=500,
            recursive=True,
            max_depth=max_depth,
            folder_id=folder_id,
        )
        files = [entry for entry in listing["items"] if entry.get("type") != "folder"]
        file_limit_reached = len(files) > self.max_files
        files = files[: self.max_files]

        created = create_local_directory(
            self.local_files_root,
            parent_directory=local_directory,
            folder_name=root_name,
        )
        destination_root = resolve_local_directory(
            self.local_files_root, created["relative_path"]
        )
        downloaded = 0
        failed = 0
        skipped = 0
        total_bytes = 0
        results: list[dict[str, Any]] = []

        for entry in listing["items"]:
            if entry.get("type") != "folder":
                continue
            try:
                path = entry.get("path")
                if not isinstance(path, list):
                    raise DriveAPIError("Drive returned incomplete folder metadata")
                parts = [
                    _safe_component(part, field="Drive folder name") for part in path
                ]
                folder_target = destination_root.joinpath(*parts).resolve()
                folder_target.relative_to(destination_root)
                folder_target.mkdir(parents=True, exist_ok=True)
            except (DriveAPIError, OSError, ValueError) as exc:
                failed += 1
                results.append(
                    {
                        "status": "failed",
                        "drive_id": entry.get("id"),
                        "name": str(entry.get("title") or "Unknown folder"),
                        "error": str(exc),
                    }
                )

        for entry in files:
            item_id = entry.get("id")
            path = entry.get("path")
            filename_value = entry.get("filename") or entry.get("title")
            try:
                if not isinstance(item_id, str) or not isinstance(path, list):
                    raise DriveAPIError("Drive returned incomplete file metadata")
                parent_parts = [
                    _safe_component(part, field="Drive folder name")
                    for part in path[:-1]
                ]
                filename = _safe_component(filename_value, field="Drive filename")
                target_parent = destination_root.joinpath(*parent_parts)
                target_parent.mkdir(parents=True, exist_ok=True)
                target = (target_parent / filename).resolve()
                target.relative_to(destination_root)
                announced_size = entry.get("size")
                if isinstance(announced_size, int) and announced_size > self.max_file_bytes:
                    skipped += 1
                    results.append(
                        {"status": "skipped", "name": filename, "reason": "file_too_large"}
                    )
                    continue
                remaining = self.max_total_bytes - total_bytes
                if remaining < 1 or (
                    isinstance(announced_size, int) and announced_size > remaining
                ):
                    skipped += 1
                    results.append(
                        {"status": "skipped", "name": filename, "reason": "total_size_limit"}
                    )
                    continue
                data = await asyncio.to_thread(
                    download_drive_file,
                    self.base_url,
                    self.session_id,
                    item_id,
                    max_bytes=min(self.max_file_bytes, remaining),
                )
                try:
                    with target.open("xb") as output:
                        output.write(data)
                except FileExistsError as exc:
                    raise LocalFilesError("A local file already exists at this path") from exc
                total_bytes += len(data)
                downloaded += 1
                results.append(
                    {
                        "status": "downloaded",
                        "drive_id": item_id,
                        "relative_path": target.relative_to(
                            self.local_files_root.expanduser().resolve()
                        ).as_posix(),
                        "bytes_written": len(data),
                    }
                )
            except (DriveAPIError, LocalFilesError, OSError, ValueError) as exc:
                failed += 1
                results.append(
                    {
                        "status": "failed",
                        "drive_id": item_id,
                        "name": str(filename_value or "Unknown"),
                        "error": str(exc),
                    }
                )

        limited = bool(
            listing.get("truncated")
            or file_limit_reached
            or skipped
        )
        complete = not limited and failed == 0
        return {
            "status": "downloaded" if complete else "partially_downloaded",
            "drive_folder_id": folder_id,
            "destination_relative_path": created["relative_path"],
            "downloaded": downloaded,
            "failed": failed,
            "skipped": skipped,
            "bytes_written": total_bytes,
            "complete": complete,
            "limited": limited,
            "source_limitation": listing.get("limitation"),
            "results": results,
            "artifact": Artifact(
                kind="folder",
                location="local",
                reference=created["relative_path"],
                media_type="inode/directory",
                name=root_name,
            ).tool_value(),
        }
