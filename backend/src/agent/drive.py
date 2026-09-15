"""Drive specialist agent and its API call."""

from __future__ import annotations

import json
from collections import deque
from http.cookies import SimpleCookie
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
from uuid import UUID

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError


def _read_json(request: Request, *, service: str, timeout: float) -> dict[str, Any]:
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise DriveAPIError(
            f"{service} returned HTTP {exc.code} for GET {request.full_url}"
        ) from exc
    except URLError as exc:
        raise DriveAPIError(f"Could not reach {request.full_url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise DriveAPIError(
            f"{service} returned invalid JSON from {request.full_url}"
        ) from exc

    if not isinstance(payload, dict):
        raise DriveAPIError(
            f"{service} returned {type(payload).__name__}; expected an object"
        )
    return payload


def get_drive_config(base_url: str, *, timeout: float = 10.0) -> dict[str, Any]:
    endpoint = urljoin(f"{base_url.rstrip('/')}/", "api/v1.0/config/")
    request = Request(endpoint, headers={"Accept": "application/json"}, method="GET")
    return _read_json(request, service="Drive", timeout=timeout)


def list_drive_items(
    base_url: str,
    session_id: str,
    *,
    limit: int = 100,
    recursive: bool = True,
    max_depth: int = 5,
    folder_id: str | None = None,
    timeout: float = 10.0,
) -> dict[str, Any]:
    """List Drive items, optionally traversing descendants breadth-first."""
    if not session_id:
        raise DriveAPIError(
            "Drive user authentication is missing. Set DRIVE_SESSION_ID to the "
            "value of your drive_sessionid cookie and restart the backend."
        )
    if not 1 <= limit <= 500:
        raise DriveAPIError("limit must be between 1 and 500")
    if not 0 <= max_depth <= 10:
        raise DriveAPIError("max_depth must be between 0 and 10")
    if folder_id is not None:
        try:
            UUID(folder_id)
        except (ValueError, AttributeError) as exc:
            raise DriveAPIError("folder_id must be a valid UUID") from exc

    cookie = SimpleCookie({"drive_sessionid": session_id}).output(header="").strip()
    fields = (
        "id",
        "title",
        "type",
        "filename",
        "mimetype",
        "size",
        "updated_at",
        "url_permalink",
    )
    items: list[dict[str, Any]] = []
    # (parent id, parent display path, depth of the children being fetched)
    pending: deque[tuple[str | None, list[str], int]] = deque(
        [(folder_id, [], 0)]
    )
    visited_folders: set[str] = set()
    root_count = 0
    truncated = False

    while pending and len(items) < limit:
        parent_id, parent_path, depth = pending.popleft()
        if parent_id is not None:
            if parent_id in visited_folders:
                continue
            visited_folders.add(parent_id)

        page = 1
        while len(items) < limit:
            page_size = min(100, limit - len(items))
            query_values = {"page_size": page_size}
            if page > 1:
                query_values["page"] = page
            query = urlencode(query_values)
            path = (
                f"api/v1.0/items/{parent_id}/children/"
                if parent_id is not None
                else "api/v1.0/items/"
            )
            endpoint = urljoin(f"{base_url.rstrip('/')}/", path)
            request = Request(
                f"{endpoint}?{query}",
                headers={"Accept": "application/json", "Cookie": cookie},
                method="GET",
            )
            payload = _read_json(request, service="Drive", timeout=timeout)
            results = payload.get("results")
            if not isinstance(results, list):
                raise DriveAPIError("Drive item list has no results array")
            if parent_id is None and page == 1:
                count = payload.get("count")
                root_count = count if isinstance(count, int) else len(results)

            for item in results:
                if not isinstance(item, dict):
                    continue
                name = item.get("title") or item.get("filename") or "Untitled"
                item_path = [*parent_path, str(name)]
                compact_item = {field: item.get(field) for field in fields}
                compact_item.update(
                    {
                        "parent_id": parent_id,
                        "depth": depth,
                        "path": item_path,
                    }
                )
                items.append(compact_item)

                item_id = item.get("id")
                if (
                    recursive
                    and depth < max_depth
                    and item.get("type") == "folder"
                    and isinstance(item_id, str)
                ):
                    pending.append((item_id, item_path, depth + 1))

                if len(items) >= limit:
                    truncated = payload.get("next") is not None or bool(pending)
                    break

            if len(items) >= limit or payload.get("next") is None:
                break
            page += 1

    return {
        "count": len(items),
        "returned": len(items),
        "top_level_count": root_count,
        "recursive": recursive,
        "max_depth": max_depth,
        "truncated": truncated,
        "items": items,
    }


class DriveConfigAgent(SpecialistAgent):
    name = "drive_get_config"
    description = (
        "Read the current public configuration of the La Suite Drive instance. "
        "Use this only for Drive languages, feature flags, environment, and public URLs."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    }

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        if arguments:
            raise DriveAPIError("drive_get_config does not accept arguments")
        return get_drive_config(self.base_url)


class DriveListItemsAgent(SpecialistAgent):
    name = "drive_list_items"
    description = (
        "List the authenticated user's files and folders in La Suite Drive, "
        "including nested folder contents by default. Use this for requests such "
        "as 'what is in my Drive?', 'show everything in my Drive', or 'what is in "
        "this Drive folder?'. This reads Drive, not the computer's local filesystem."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 500,
                "description": "Maximum total number of items to return.",
            },
            "recursive": {
                "type": "boolean",
                "description": "Whether to traverse nested folders. Defaults to true.",
            },
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 10,
                "description": "Maximum nested depth. Zero lists only one level.",
            },
            "folder_id": {
                "type": "string",
                "format": "uuid",
                "description": "Optional Drive folder UUID to inspect instead of the root.",
            },
        },
        "additionalProperties": False,
    }

    def __init__(self, base_url: str, session_id: str | None) -> None:
        self.base_url = base_url
        self.session_id = session_id

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        limit = arguments.get("limit", 100)
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise DriveAPIError("limit must be an integer")
        recursive = arguments.get("recursive", True)
        if not isinstance(recursive, bool):
            raise DriveAPIError("recursive must be a boolean")
        max_depth = arguments.get("max_depth", 5)
        if not isinstance(max_depth, int) or isinstance(max_depth, bool):
            raise DriveAPIError("max_depth must be an integer")
        folder_id = arguments.get("folder_id")
        if folder_id is not None and not isinstance(folder_id, str):
            raise DriveAPIError("folder_id must be a string")
        return list_drive_items(
            self.base_url,
            self.session_id or "",
            limit=limit,
            recursive=recursive,
            max_depth=max_depth,
            folder_id=folder_id,
        )
