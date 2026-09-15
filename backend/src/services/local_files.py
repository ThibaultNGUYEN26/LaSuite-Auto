"""Bounded local-files access restricted to one configured root directory."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent.errors import LocalFilesError

MAX_TRAVERSAL_DEPTH = 5


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
            children = sorted(directory.iterdir(), key=lambda path: path.name.casefold())
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
            items.append(
                {
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
            )
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
        limitations.append(
            f"Folder traversal stopped at depth {MAX_TRAVERSAL_DEPTH}; deeper folders "
            "were not checked."
        )
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
        "items": items,
    }


def read_local_pdf(root: Path, relative_path: str, *, max_bytes: int) -> bytes:
    path = resolve_local_file(root, relative_path)
    if path.suffix.lower() != ".pdf":
        raise LocalFilesError("Unsupported file type. Only PDF files are supported.")
    size = path.stat().st_size
    if size > max_bytes:
        raise LocalFilesError(
            f"Local PDF exceeds the configured {max_bytes}-byte read limit"
        )
    try:
        data = path.read_bytes()
    except PermissionError as exc:
        raise LocalFilesError("Permission denied") from exc
    except FileNotFoundError as exc:
        raise LocalFilesError("File not found") from exc
    if len(data) > max_bytes:
        raise LocalFilesError(
            f"Local PDF exceeds the configured {max_bytes}-byte read limit"
        )
    if not data.startswith(b"%PDF-"):
        raise LocalFilesError("The selected local file is not a valid PDF")
    return data
