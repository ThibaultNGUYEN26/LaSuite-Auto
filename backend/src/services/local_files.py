"""Bounded local-files access restricted to one configured root directory."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import mimetypes
from pathlib import Path
import re
from typing import Any

from agent.artifacts import Artifact
from agent.errors import LocalFilesError
from services.text_content import decode_text_content

MAX_TRAVERSAL_DEPTH = 5
EXTENSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,15}$")
WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


def _root_directory(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise LocalFilesError(f"Configured local-files root does not exist: {resolved}")
    if not resolved.is_dir():
        raise LocalFilesError(f"Configured local-files root is not a directory: {resolved}")
    return resolved


def resolve_local_file(root: Path, relative_path: str) -> Path:
    """Resolve a model-provided relative path without permitting root escape."""
    if not relative_path or Path(relative_path).is_absolute():
        raise LocalFilesError("relative_path must be a non-empty relative path")
    resolved_root = _root_directory(root)
    candidate = (resolved_root / relative_path).resolve()
    try:
        candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise LocalFilesError("relative_path escapes the configured local-files root") from exc
    if not candidate.exists():
        raise LocalFilesError("File does not exist")
    if not candidate.is_file():
        raise LocalFilesError("Path is not a file")
    return candidate


def resolve_local_directory(root: Path, relative_directory: str = ".") -> Path:
    """Resolve a directory below the configured root without permitting escape."""
    if Path(relative_directory).is_absolute():
        raise LocalFilesError("directory must be relative to the local-files root")
    resolved_root = _root_directory(root)
    candidate = (resolved_root / relative_directory).resolve()
    try:
        candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise LocalFilesError("directory escapes the configured local-files root") from exc
    if not candidate.exists():
        raise LocalFilesError("Directory does not exist")
    if not candidate.is_dir():
        raise LocalFilesError("Path is not a directory")
    return candidate


def list_local_items(
    root: Path,
    *,
    directory: str = ".",
    limit: int = 100,
    recursive: bool = True,
    max_depth: int = 5,
) -> dict[str, Any]:
    resolved_root = _root_directory(root)
    start_directory = resolve_local_directory(resolved_root, directory)
    if not 1 <= limit <= 500:
        raise LocalFilesError("limit must be between 1 and 500")
    if max_depth < 0:
        raise LocalFilesError("max_depth must be zero or greater")
    requested_max_depth = max_depth
    max_depth = min(max_depth, MAX_TRAVERSAL_DEPTH)

    items: list[dict[str, Any]] = []
    pending: deque[tuple[Path, int]] = deque([(start_directory, 0)])
    truncated = False
    depth_limited = recursive and requested_max_depth > MAX_TRAVERSAL_DEPTH
    while pending and len(items) < limit:
        directory, depth = pending.popleft()
        try:
            def _mtime_or_zero(path: Path) -> float:
                try:
                    return path.stat().st_mtime
                except OSError:
                    return 0.0

            children = sorted(directory.iterdir(), key=_mtime_or_zero, reverse=True)
        except PermissionError:
            continue
        for child in children:
            try:
                resolved_child = child.resolve()
                resolved_child.relative_to(resolved_root)
                is_directory = resolved_child.is_dir()
                is_file = resolved_child.is_file()
                stat = resolved_child.stat()
            except (OSError, ValueError):
                continue
            if not is_directory and not is_file:
                continue
            relative_path = resolved_child.relative_to(resolved_root).as_posix()
            item = {
                    "name": child.name,
                    "type": "folder" if is_directory else "file",
                    "relative_path": relative_path,
                    "extension": child.suffix.lower() if is_file else None,
                    "size": stat.st_size if is_file else None,
                    "modified_at": datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ).isoformat(),
                    "depth": depth,
                }
            if is_file:
                item["artifact"] = Artifact(
                    kind="file",
                    location="local",
                    reference=relative_path,
                    media_type=(
                        mimetypes.guess_type(child.name)[0]
                        or "application/octet-stream"
                    ),
                    name=child.name,
                ).tool_value()
            items.append(item)
            if recursive and is_directory and depth < max_depth:
                pending.append((resolved_child, depth + 1))
            elif recursive and is_directory and depth >= max_depth:
                depth_limited = True
            if len(items) >= limit:
                truncated = True
                break
    item_limit_reached = truncated or bool(pending)
    limitations: list[str] = []
    if depth_limited:
        limitations.append("Some folders are nested further inside and were not checked yet.")
    if item_limit_reached:
        limitations.append(f"Only the first {limit} items were returned.")
    return {
        "root_name": resolved_root.name,
        "directory": start_directory.relative_to(resolved_root).as_posix() or ".",
        "count": len(items),
        "recursive": recursive,
        "max_depth": max_depth,
        "requested_max_depth": requested_max_depth,
        "depth_limited": depth_limited,
        "item_limit_reached": item_limit_reached,
        "truncated": depth_limited or item_limit_reached,
        "complete": not depth_limited and not item_limit_reached,
        "limitation": " ".join(limitations) or None,
        "suggested_question": (
            "Would you like me to focus on a specific folder, or show everything "
            "I found so far?"
            if depth_limited
            else None
        ),
        "items": items,
    }


def read_local_file(root: Path, relative_path: str, *, max_bytes: int) -> bytes:
    path = resolve_local_file(root, relative_path)
    size = path.stat().st_size
    if size > max_bytes:
        raise LocalFilesError(
            f"Local file exceeds the configured {max_bytes}-byte read limit"
        )
    try:
        data = path.read_bytes()
    except PermissionError as exc:
        raise LocalFilesError("Permission denied") from exc
    except FileNotFoundError as exc:
        raise LocalFilesError("File not found") from exc
    if len(data) > max_bytes:
        raise LocalFilesError(
            f"Local file exceeds the configured {max_bytes}-byte read limit"
        )
    return data


def read_local_text(
    root: Path,
    relative_path: str,
    *,
    max_bytes: int,
    max_characters: int,
) -> dict[str, Any]:
    """Read a bounded text-based file with BOM-aware Unicode decoding."""
    path = resolve_local_file(root, relative_path)
    data = read_local_file(root, relative_path, max_bytes=max_bytes)
    returned_content, used_encoding, total_characters, truncated = decode_text_content(
        data,
        filename=path.name,
        max_characters=max_characters,
        error_type=LocalFilesError,
    )
    relative = path.relative_to(_root_directory(root)).as_posix()
    artifact = Artifact(
        kind="file",
        location="local",
        reference=relative,
        media_type=mimetypes.guess_type(path.name)[0] or "text/plain",
        name=path.name,
    )
    return {
        "status": "read",
        "relative_path": relative,
        "name": path.name,
        "encoding": used_encoding,
        "characters": total_characters,
        "returned_characters": len(returned_content),
        "truncated": truncated,
        "content": returned_content,
        "artifact": artifact.tool_value(),
    }


def read_local_pdf(root: Path, relative_path: str, *, max_bytes: int) -> bytes:
    path = resolve_local_file(root, relative_path)
    if path.suffix.lower() != ".pdf":
        raise LocalFilesError("Unsupported file type. Only PDF files are supported.")
    data = read_local_file(root, relative_path, max_bytes=max_bytes)
    if not data.startswith(b"%PDF-"):
        raise LocalFilesError("The selected local file is not a valid PDF")
    return data


def prepare_new_local_file(
    root: Path,
    *,
    directory: str,
    file_name: str,
    extension: str,
) -> tuple[Path, str]:
    """Validate a requested new file name/extension and return its target path.

    The returned path does not exist yet. Callers must create it themselves,
    ideally with an exclusive ("x") open mode, so an existing file already at
    that path is never silently overwritten.
    """
    target_directory = resolve_local_directory(root, directory)
    clean_name = file_name.strip()
    clean_extension = extension.strip().removeprefix(".")
    if (
        not clean_name
        or clean_name in {".", ".."}
        or Path(clean_name).name != clean_name
        or any(character in clean_name for character in '<>:"/\\|?*')
        or clean_name.endswith((" ", "."))
    ):
        raise LocalFilesError("file_name contains invalid characters")
    if clean_name.upper() in WINDOWS_RESERVED_NAMES:
        raise LocalFilesError("file_name is reserved by Windows")
    if not EXTENSION_PATTERN.fullmatch(clean_extension):
        raise LocalFilesError("extension must contain only letters, numbers, _ or -")

    target = (target_directory / f"{clean_name}.{clean_extension}").resolve()
    resolved_root = _root_directory(root)
    try:
        relative_path = target.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise LocalFilesError("Target path escapes the configured local-files root") from exc
    return target, relative_path


def create_local_text_file(
    root: Path,
    *,
    directory: str,
    file_name: str,
    extension: str,
    content: str,
    max_bytes: int,
) -> dict[str, Any]:
    """Create one UTF-8 file without overwriting an existing path."""
    encoded = content.encode("utf-8")
    if len(encoded) > max_bytes:
        raise LocalFilesError(
            f"File content exceeds the configured {max_bytes}-byte creation limit"
        )
    target, relative_path = prepare_new_local_file(
        root, directory=directory, file_name=file_name, extension=extension
    )
    try:
        with target.open("x", encoding="utf-8", newline="") as file:
            file.write(content)
    except FileExistsError as exc:
        raise LocalFilesError(
            "A file with this name already exists. Choose another name."
        ) from exc
    except PermissionError as exc:
        raise LocalFilesError("Permission denied") from exc
    artifact = Artifact(
        kind="file",
        location="local",
        reference=relative_path,
        media_type=mimetypes.guess_type(target.name)[0] or "text/plain",
        name=target.name,
    )
    return {
        "status": "created",
        "relative_path": relative_path,
        "extension": target.suffix,
        "bytes_written": len(encoded),
        "artifact": artifact.tool_value(),
    }


def create_local_binary_file(
    root: Path,
    *,
    directory: str,
    file_name: str,
    extension: str,
    data: bytes,
    max_bytes: int,
    media_type: str,
) -> dict[str, Any]:
    """Create one binary file without overwriting an existing path."""
    if not isinstance(data, bytes):
        raise LocalFilesError("data must be bytes")
    if len(data) > max_bytes:
        raise LocalFilesError(
            f"File content exceeds the configured {max_bytes}-byte creation limit"
        )
    target_directory = resolve_local_directory(root, directory)
    clean_name = file_name.strip()
    clean_extension = extension.strip().removeprefix(".")
    if (
        not clean_name
        or clean_name in {".", ".."}
        or Path(clean_name).name != clean_name
        or any(character in clean_name for character in '<>:"/\\|?*')
        or clean_name.endswith((" ", "."))
    ):
        raise LocalFilesError("file_name contains invalid characters")
    if clean_name.upper() in WINDOWS_RESERVED_NAMES:
        raise LocalFilesError("file_name is reserved by Windows")
    if not EXTENSION_PATTERN.fullmatch(clean_extension):
        raise LocalFilesError("extension must contain only letters, numbers, _ or -")

    target = (target_directory / f"{clean_name}.{clean_extension}").resolve()
    resolved_root = _root_directory(root)
    try:
        relative_path = target.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise LocalFilesError("Target path escapes the configured local-files root") from exc
    try:
        with target.open("xb") as file:
            file.write(data)
    except FileExistsError as exc:
        raise LocalFilesError(
            "A file with this name already exists. Choose another name."
        ) from exc
    except PermissionError as exc:
        raise LocalFilesError("Permission denied") from exc
    artifact = Artifact(
        kind="file",
        location="local",
        reference=relative_path,
        media_type=media_type,
        name=target.name,
    )
    return {
        "status": "created",
        "relative_path": relative_path,
        "extension": f".{clean_extension}",
        "bytes_written": len(data),
        "artifact": artifact.tool_value(),
    }


def rename_local_file(
    root: Path,
    *,
    relative_path: str,
    new_name: str,
) -> dict[str, Any]:
    """Rename one file in place without moving it or overwriting another file."""
    source = resolve_local_file(root, relative_path)
    if not isinstance(new_name, str):
        raise LocalFilesError("new_name must be a string")
    clean_name = new_name.strip()
    if (
        not clean_name
        or clean_name in {".", ".."}
        or Path(clean_name).name != clean_name
        or any(character in clean_name for character in '<>:"/\\|?*')
        or clean_name.endswith((" ", "."))
    ):
        raise LocalFilesError("new_name contains invalid characters")
    if not Path(clean_name).suffix and source.suffix:
        clean_name = f"{clean_name}{source.suffix}"
    if Path(clean_name).stem.upper() in WINDOWS_RESERVED_NAMES:
        raise LocalFilesError("new_name is reserved by Windows")

    target = source.with_name(clean_name)
    if target == source:
        raise LocalFilesError("The file already has that name")
    if target.exists():
        raise LocalFilesError(
            "A file with the requested name already exists in this directory"
        )
    resolved_root = _root_directory(root)
    try:
        old_relative_path = source.relative_to(resolved_root).as_posix()
        new_relative_path = target.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise LocalFilesError("Rename target escapes the configured local-files root") from exc
    try:
        source.rename(target)
    except FileNotFoundError as exc:
        raise LocalFilesError("File no longer exists") from exc
    except PermissionError as exc:
        raise LocalFilesError("Permission denied") from exc
    except OSError as exc:
        raise LocalFilesError(f"Could not rename file: {exc}") from exc

    artifact = Artifact(
        kind="file",
        location="local",
        reference=new_relative_path,
        media_type=mimetypes.guess_type(target.name)[0] or "application/octet-stream",
        name=target.name,
    )
    return {
        "status": "renamed",
        "old_relative_path": old_relative_path,
        "relative_path": new_relative_path,
        "name": target.name,
        "artifact": artifact.tool_value(),
    }
