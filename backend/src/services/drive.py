"""Low-level, authenticated access to La Suite Drive."""

from __future__ import annotations

import json
from collections import deque
from http.cookies import SimpleCookie
from typing import Any, BinaryIO
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen
from uuid import UUID

from agent.errors import DriveAPIError

MAX_TRAVERSAL_DEPTH = 5


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


def _session_cookie(session_id: str) -> str:
    if not session_id:
        raise DriveAPIError(
            "Drive user authentication is missing. Set DRIVE_SESSION_ID to the "
            "value of your drive_sessionid cookie and restart the backend."
        )
    return SimpleCookie({"drive_sessionid": session_id}).output(header="").strip()


def _validate_uuid(value: str, *, field: str) -> None:
    try:
        UUID(value)
    except (ValueError, AttributeError) as exc:
        raise DriveAPIError(f"{field} must be a valid UUID") from exc


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
    cookie = _session_cookie(session_id)
    if not 1 <= limit <= 500:
        raise DriveAPIError("limit must be between 1 and 500")
    if max_depth < 0:
        raise DriveAPIError("max_depth must be zero or greater")
    requested_max_depth = max_depth
    max_depth = min(max_depth, MAX_TRAVERSAL_DEPTH)
    if folder_id is not None:
        _validate_uuid(folder_id, field="folder_id")

    fields = (
        "id", "title", "type", "filename", "mimetype", "size",
        "updated_at", "url_permalink",
    )
    items: list[dict[str, Any]] = []
    pending: deque[tuple[str | None, list[str], int]] = deque([(folder_id, [], 0)])
    visited_folders: set[str] = set()
    root_count = 0
    truncated = False
    depth_limited = recursive and requested_max_depth > MAX_TRAVERSAL_DEPTH

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
            path = (
                f"api/v1.0/items/{parent_id}/children/"
                if parent_id is not None else "api/v1.0/items/"
            )
            endpoint = urljoin(f"{base_url.rstrip('/')}/", path)
            request = Request(
                f"{endpoint}?{urlencode(query_values)}",
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
                compact_item.update({"parent_id": parent_id, "depth": depth, "path": item_path})
                items.append(compact_item)
                item_id = item.get("id")
                if (
                    recursive and depth < max_depth and item.get("type") == "folder"
                    and isinstance(item_id, str)
                ):
                    pending.append((item_id, item_path, depth + 1))
                elif recursive and depth >= max_depth and item.get("type") == "folder":
                    depth_limited = True
                if len(items) >= limit:
                    truncated = payload.get("next") is not None or bool(pending)
                    break
            if len(items) >= limit or payload.get("next") is None:
                break
            page += 1
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
        "count": len(items), "returned": len(items), "top_level_count": root_count,
        "recursive": recursive, "max_depth": max_depth,
        "requested_max_depth": requested_max_depth,
        "depth_limited": depth_limited,
        "item_limit_reached": item_limit_reached,
        "truncated": depth_limited or item_limit_reached,
        "complete": not depth_limited and not item_limit_reached,
        "limitation": " ".join(limitations) or None,
        "items": items,
    }


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _read_limited(response: BinaryIO, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(64 * 1024, max_bytes + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > max_bytes:
            raise DriveAPIError(
                f"Drive PDF exceeds the configured {max_bytes}-byte download limit"
            )
    return b"".join(chunks)


def download_drive_pdf(
    base_url: str,
    session_id: str,
    item_id: str,
    *,
    max_bytes: int = 20 * 1024 * 1024,
    timeout: float = 30.0,
) -> bytes:
    """Download one PDF without forwarding the session cookie across redirects."""
    cookie = _session_cookie(session_id)
    _validate_uuid(item_id, field="item_id")
    endpoint = urljoin(
        f"{base_url.rstrip('/')}/", f"api/v1.0/items/{item_id}/download/"
    )
    request = Request(
        endpoint,
        # This DRF action negotiates its redirect as an API response. Asking
        # for application/pdf is rejected with HTTP 406 before the file URL is
        # generated; the redirected object-storage request fetches the PDF.
        headers={"Accept": "application/json", "Cookie": cookie},
        method="GET",
    )
    opener = build_opener(_NoRedirect())
    try:
        response = opener.open(request, timeout=timeout)
    except HTTPError as exc:
        if exc.code not in {301, 302, 303, 307, 308}:
            raise DriveAPIError(f"Drive returned HTTP {exc.code} for GET {endpoint}") from exc
        location = exc.headers.get("Location")
        if not location:
            raise DriveAPIError("Drive download redirect has no Location header") from exc
        target = urljoin(endpoint, location)
        source_url = urlparse(endpoint)
        target_url = urlparse(target)
        if target_url.scheme not in {"http", "https"}:
            raise DriveAPIError("Drive returned an unsafe download URL") from exc
        # Do not force an Accept header here. The development media proxy
        # returns HTTP 500 for ``Accept: application/pdf`` but serves the same
        # authenticated request successfully with normal browser negotiation.
        redirect_headers: dict[str, str] = {}
        same_hostname = source_url.hostname == target_url.hostname
        no_https_downgrade = source_url.scheme != "https" or target_url.scheme == "https"
        if same_hostname and no_https_downgrade:
            # Cookies are scoped by hostname, not port. Drive's development
            # media proxy runs on another port and requires the same session
            # cookie, just as a browser would send it. Never send the cookie to
            # a redirect on a different hostname or across an HTTPS downgrade.
            redirect_headers["Cookie"] = cookie
        clean_request = Request(target, headers=redirect_headers, method="GET")
        try:
            response = urlopen(clean_request, timeout=timeout)
        except HTTPError as redirect_exc:
            raise DriveAPIError(
                f"Drive file storage returned HTTP {redirect_exc.code}"
            ) from redirect_exc
        except URLError as redirect_exc:
            raise DriveAPIError(
                f"Could not reach Drive file storage: {redirect_exc.reason}"
            ) from redirect_exc
    except URLError as exc:
        raise DriveAPIError(f"Could not reach {endpoint}: {exc.reason}") from exc

    with response:
        content_length = response.headers.get("Content-Length")
        if content_length:
            try:
                if int(content_length) > max_bytes:
                    raise DriveAPIError(
                        f"Drive PDF exceeds the configured {max_bytes}-byte download limit"
                    )
            except ValueError:
                pass
        data = _read_limited(response, max_bytes)
    if not data.startswith(b"%PDF-"):
        raise DriveAPIError("The selected Drive item is not a valid PDF file")
    return data
