"""Low-level, authenticated access to La Suite Drive."""

from __future__ import annotations

import json
import mimetypes
from collections import deque
from contextlib import contextmanager
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any, BinaryIO, Iterator
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urljoin, urlparse
from urllib.request import Request, urlopen
from uuid import UUID

import openapi_client
import urllib3
from openapi_client.api.api_api import ApiApi as GeneratedDriveApi
from openapi_client.exceptions import ApiException as GeneratedDriveApiException
from openapi_client.models.create_item_request import CreateItemRequest
from openapi_client.models.item_request import ItemRequest
from openapi_client.models.list_item_request import ListItemRequest
from openapi_client.models.patched_item_request import PatchedItemRequest
from openapi_client.models.type_enum import TypeEnum

from agent.artifacts import Artifact
from agent.errors import DriveAPIError
from services.text_content import decode_text_content

MAX_TRAVERSAL_DEPTH = 5


def _session_required(session_id: str) -> None:
    if not session_id:
        raise DriveAPIError(
            "Drive user authentication is missing. Set DRIVE_SESSION_ID to the "
            "value of your drive_sessionid cookie and restart the backend."
        )


def _session_cookie_header(session_id: str) -> str:
    """Build a cookie only for a same-host object-storage redirect."""
    _session_required(session_id)
    return SimpleCookie({"drive_sessionid": session_id}).output(header="").strip()


@contextmanager
def _drive_api(
    base_url: str,
    session_id: str | None = None,
    *,
    csrf_token: str | None = None,
    follow_redirects: bool = True,
) -> Iterator[GeneratedDriveApi]:
    """Build the generated Drive client with credentials kept outside the SDK."""
    if session_id is not None:
        _session_required(session_id)
    retries = None
    if not follow_redirects:
        retries = urllib3.util.Retry(redirect=0, raise_on_redirect=False)
    configuration = openapi_client.Configuration(
        host=base_url.rstrip("/"),
        api_key={"cookieAuth": session_id} if session_id else None,
        ignore_operation_servers=True,
        retries=retries,
    )
    cookie = f"csrftoken={csrf_token}" if csrf_token else None
    with openapi_client.ApiClient(configuration, cookie=cookie) as api_client:
        yield GeneratedDriveApi(api_client)


def _csrf_headers(csrf_token: str | None) -> dict[str, str] | None:
    return {"X-CSRFToken": csrf_token} if csrf_token else None


def _raise_for_generated_response(response: Any, *, action: str) -> None:
    status = getattr(response, "status", None)
    if isinstance(status, int) and not 200 <= status < 300:
        raise DriveAPIError(f"Drive returned HTTP {status} while {action}")


def _generated_json(response: Any, *, action: str) -> dict[str, Any]:
    """Decode a generated raw response when the OpenAPI response model is wrong."""
    _raise_for_generated_response(response, action=action)
    try:
        raw = response.read()
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DriveAPIError(f"Drive returned invalid JSON while {action}") from exc
    if not isinstance(payload, dict):
        raise DriveAPIError(f"Drive returned an invalid object while {action}")
    return payload


def _generated_call_error(exc: Exception, *, action: str) -> DriveAPIError:
    if isinstance(exc, GeneratedDriveApiException) and exc.status:
        return DriveAPIError(f"Drive returned HTTP {exc.status} while {action}")
    return DriveAPIError(f"Could not reach Drive while {action}: {exc}")


def _generated_next_page(
    drive_api: GeneratedDriveApi,
    next_url: str,
    *,
    timeout: float,
) -> Any:
    """Follow an API-provided pagination URL with the generated client's auth."""
    parsed = urlparse(next_url)
    configured = urlparse(drive_api.api_client.configuration.host)
    if (
        parsed.scheme not in {"http", "https"}
        or parsed.scheme != configured.scheme
        or parsed.netloc != configured.netloc
    ):
        raise DriveAPIError("Drive returned an unsafe pagination URL")
    request = drive_api.api_client.param_serialize(
        method="GET",
        resource_path=parsed.path,
        query_params=parse_qsl(parsed.query, keep_blank_values=True),
        header_params={"Accept": "application/json"},
        auth_settings=["cookieAuth"],
    )
    return drive_api.api_client.call_api(*request, _request_timeout=timeout)


def _validate_uuid(value: str, *, field: str) -> None:
    try:
        UUID(value)
    except (ValueError, AttributeError) as exc:
        raise DriveAPIError(f"{field} must be a valid UUID") from exc


def get_drive_config(base_url: str, *, timeout: float = 10.0) -> dict[str, Any]:
    try:
        with _drive_api(base_url) as drive_api:
            response = drive_api.api_v1_0_config_retrieve_without_preload_content(
                _request_timeout=timeout
            )
            return _generated_json(response, action="reading configuration")
    except (GeneratedDriveApiException, urllib3.exceptions.HTTPError) as exc:
        raise _generated_call_error(exc, action="reading configuration") from exc


def get_drive_item(
    base_url: str,
    session_id: str,
    item_id: str,
    *,
    timeout: float = 10.0,
) -> dict[str, Any]:
    """Read metadata for one authenticated Drive item."""
    _validate_uuid(item_id, field="item_id")
    try:
        with _drive_api(base_url, session_id) as drive_api:
            response = drive_api.api_v1_0_items_retrieve_without_preload_content(
                UUID(item_id), _request_timeout=timeout
            )
            return _generated_json(response, action="reading an item")
    except (GeneratedDriveApiException, urllib3.exceptions.HTTPError) as exc:
        raise _generated_call_error(exc, action="reading an item") from exc


def create_drive_folder(
    base_url: str,
    session_id: str,
    *,
    title: str,
    parent_id: str | None = None,
    csrf_token: str | None = None,
    timeout: float = 10.0,
) -> dict[str, Any]:
    """Create a Drive folder through the generated OpenAPI client."""
    clean_title = title.strip()
    if (
        not clean_title
        or len(clean_title) > 255
        or clean_title in {".", ".."}
        or any(ord(character) < 32 for character in clean_title)
        or "/" in clean_title
        or "\\" in clean_title
    ):
        raise DriveAPIError("title contains invalid characters")
    _session_required(session_id)
    parent_uuid = None
    if parent_id is not None:
        _validate_uuid(parent_id, field="parent_id")
        parent_uuid = UUID(parent_id)

    try:
        with _drive_api(
            base_url, session_id, csrf_token=csrf_token
        ) as drive_api:
            if parent_uuid is None:
                response = drive_api.api_v1_0_items_create_without_preload_content(
                    CreateItemRequest(title=clean_title, type=TypeEnum.FOLDER),
                    _request_timeout=timeout,
                    _headers=_csrf_headers(csrf_token),
                )
            else:
                response = drive_api.api_v1_0_items_children_create_without_preload_content(
                    parent_uuid,
                    ListItemRequest(title=clean_title),
                    _request_timeout=timeout,
                    _headers=_csrf_headers(csrf_token),
                )
            item = _generated_json(response, action="creating a folder")
    except (GeneratedDriveApiException, urllib3.exceptions.HTTPError) as exc:
        raise _generated_call_error(exc, action="creating a folder") from exc

    item_id = item.get("id")
    if not isinstance(item_id, str):
        raise DriveAPIError("Drive folder creation response has no item ID")
    folder_title = item.get("title")
    if not isinstance(folder_title, str):
        folder_title = clean_title
    url_permalink = (
        item.get("url_permalink")
        if isinstance(item.get("url_permalink"), str)
        else None
    )
    artifact = Artifact(
        kind="folder",
        location="drive",
        reference=item_id,
        media_type="inode/directory",
        name=folder_title,
        metadata={
            "parent_id": parent_id,
            **(
                {"url_permalink": url_permalink}
                if url_permalink is not None
                else {}
            ),
        },
    )
    return {
        "status": "created",
        "id": item_id,
        "title": folder_title,
        "type": "folder",
        "parent_id": parent_id,
        "url_permalink": url_permalink,
        "artifact": artifact.tool_value(),
    }


def resolve_drive_upload_acl(
    base_url: str,
    configured_acl: str | None,
) -> str | None:
    """Resolve the storage ACL override or use Drive's public configuration."""
    upload_acl = configured_acl
    if upload_acl is None:
        config = get_drive_config(base_url)
        discovered_acl = config.get("AWS_S3_UPLOAD_ACL")
        if discovered_acl is not None and not isinstance(discovered_acl, str):
            raise DriveAPIError("Drive returned an invalid upload configuration")
        upload_acl = discovered_acl
    return None if not upload_acl or upload_acl == "default" else upload_acl


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
    _session_required(session_id)
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

    try:
        with _drive_api(base_url, session_id) as drive_api:
            while pending and len(items) < limit:
                parent_id, parent_path, depth = pending.popleft()
                if parent_id is not None:
                    if parent_id in visited_folders:
                        continue
                    visited_folders.add(parent_id)
                next_page_url: str | None = None
                page_number = 0
                while len(items) < limit:
                    if page_number == 0:
                        page_size = min(100, limit - len(items))
                        if parent_id is None:
                            response = drive_api.api_v1_0_items_list_without_preload_content(
                                page_size=page_size,
                                _request_timeout=timeout,
                            )
                        else:
                            response = drive_api.api_v1_0_items_children_retrieve_without_preload_content(
                                UUID(parent_id),
                                _request_timeout=timeout,
                            )
                    else:
                        assert next_page_url is not None
                        response = _generated_next_page(
                            drive_api, next_page_url, timeout=timeout
                        )
                    payload = _generated_json(response, action="listing items")
                    next_value = payload.get("next")
                    next_page_url = next_value if isinstance(next_value, str) else None
                    results = payload.get("results")
                    if not isinstance(results, list):
                        raise DriveAPIError("Drive item list has no results array")
                    if parent_id is None and page_number == 0:
                        count = payload.get("count")
                        root_count = count if isinstance(count, int) else len(results)
                    for item in results:
                        if not isinstance(item, dict):
                            continue
                        name = item.get("title") or item.get("filename") or "Untitled"
                        item_path = [*parent_path, str(name)]
                        compact_item = {field: item.get(field) for field in fields}
                        compact_item.update(
                            {"parent_id": parent_id, "depth": depth, "path": item_path}
                        )
                        item_id = item.get("id")
                        if isinstance(item_id, str):
                            is_folder = item.get("type") == "folder"
                            compact_item["artifact"] = Artifact(
                                kind="folder" if is_folder else "file",
                                location="drive",
                                reference=item_id,
                                media_type=(
                                    "inode/directory"
                                    if is_folder
                                    else (
                                        item.get("mimetype")
                                        if isinstance(item.get("mimetype"), str)
                                        else "application/octet-stream"
                                    )
                                ),
                                name=(
                                    str(name)
                                    if is_folder
                                    else (
                                        item.get("filename")
                                        if isinstance(item.get("filename"), str)
                                        else str(name)
                                    )
                                ),
                            ).tool_value()
                        items.append(compact_item)
                        if (
                            recursive
                            and depth < max_depth
                            and item.get("type") == "folder"
                            and isinstance(item_id, str)
                        ):
                            pending.append((item_id, item_path, depth + 1))
                        elif (
                            recursive
                            and depth >= max_depth
                            and item.get("type") == "folder"
                        ):
                            depth_limited = True
                        if len(items) >= limit:
                            truncated = next_page_url is not None or bool(pending)
                            break
                    if len(items) >= limit or next_page_url is None:
                        break
                    page_number += 1
    except (GeneratedDriveApiException, urllib3.exceptions.HTTPError) as exc:
        raise _generated_call_error(exc, action="listing items") from exc
    item_limit_reached = truncated or bool(pending)
    limitations: list[str] = []
    if depth_limited:
        limitations.append("Some folders are nested further inside and were not checked yet.")
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
        "suggested_question": (
            "Would you like me to focus on a specific folder, or show everything "
            "I found so far?"
            if depth_limited
            else None
        ),
        "items": items,
    }


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
                f"Drive file exceeds the configured {max_bytes}-byte download limit"
            )
    return b"".join(chunks)


def _read_bounded_response(
    response: Any,
    max_bytes: int,
    *,
    limit_message: str,
) -> bytes:
    content_length = response.headers.get("Content-Length")
    if content_length:
        try:
            if int(content_length) > max_bytes:
                raise DriveAPIError(limit_message)
        except ValueError:
            pass
    return _read_limited(response, max_bytes)


def download_drive_file(
    base_url: str,
    session_id: str,
    item_id: str,
    *,
    max_bytes: int = 20 * 1024 * 1024,
    timeout: float = 30.0,
) -> bytes:
    """Download one file without leaking the session cookie across hostnames."""
    _session_required(session_id)
    _validate_uuid(item_id, field="item_id")
    location: str | None = None
    try:
        with _drive_api(base_url, session_id, follow_redirects=False) as drive_api:
            response = drive_api.api_v1_0_items_download_retrieve_without_preload_content(
                UUID(item_id), _request_timeout=timeout
            )
            status = getattr(response, "status", None)
            if status in {301, 302, 303, 307, 308}:
                location = response.headers.get("Location")
                if not location:
                    raise DriveAPIError("Drive download redirect has no Location header")
            else:
                _raise_for_generated_response(response, action="downloading a file")
                with response:
                    return _read_bounded_response(
                        response,
                        max_bytes,
                        limit_message=(
                            f"Drive file exceeds the configured {max_bytes}-byte "
                            "download limit"
                        ),
                    )
    except (GeneratedDriveApiException, urllib3.exceptions.HTTPError) as exc:
        raise _generated_call_error(exc, action="downloading a file") from exc

    if location is not None:
        source_endpoint = f"{base_url.rstrip('/')}/"
        target = urljoin(source_endpoint, location)
        source_url = urlparse(source_endpoint)
        target_url = urlparse(target)
        if target_url.scheme not in {"http", "https"}:
            raise DriveAPIError("Drive returned an unsafe download URL")
        redirect_headers: dict[str, str] = {}
        same_hostname = source_url.hostname == target_url.hostname
        no_https_downgrade = source_url.scheme != "https" or target_url.scheme == "https"
        if same_hostname and no_https_downgrade:
            redirect_headers["Cookie"] = _session_cookie_header(session_id)
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
        with response:
            return _read_bounded_response(
                response,
                max_bytes,
                limit_message=(
                    f"Drive file exceeds the configured {max_bytes}-byte download limit"
                ),
            )
    raise DriveAPIError("Drive returned no downloadable content")


def download_drive_folder_archive(
    base_url: str,
    session_id: str,
    folder_id: str,
    *,
    max_bytes: int = 200 * 1024 * 1024,
    timeout: float = 120.0,
) -> bytes:
    """Stream Drive's native recursive ZIP export for one folder."""
    _session_required(session_id)
    _validate_uuid(folder_id, field="folder_id")
    try:
        with _drive_api(base_url, session_id) as drive_api:
            response = drive_api.api_v1_0_items_export_retrieve_without_preload_content(
                UUID(folder_id), _request_timeout=timeout
            )
            _raise_for_generated_response(response, action="exporting a folder")
            with response:
                data = _read_bounded_response(
                    response,
                    max_bytes,
                    limit_message=(
                        "Drive folder archive exceeds the configured download limit"
                    ),
                )
    except (GeneratedDriveApiException, urllib3.exceptions.HTTPError) as exc:
        raise _generated_call_error(exc, action="exporting a folder") from exc
    if not data.startswith(b"PK"):
        raise DriveAPIError("Drive did not return a valid ZIP folder archive")
    return data


def download_drive_pdf(
    base_url: str,
    session_id: str,
    item_id: str,
    *,
    max_bytes: int = 20 * 1024 * 1024,
    timeout: float = 30.0,
) -> bytes:
    data = download_drive_file(
        base_url,
        session_id,
        item_id,
        max_bytes=max_bytes,
        timeout=timeout,
    )
    if not data.startswith(b"%PDF-"):
        raise DriveAPIError("The selected Drive item is not a valid PDF file")
    return data


def read_drive_text(
    base_url: str,
    session_id: str,
    item_id: str,
    *,
    filename: str,
    max_bytes: int = 20 * 1024 * 1024,
    max_characters: int = 100_000,
) -> dict[str, Any]:
    """Download and decode one bounded text-based Drive file."""
    if not isinstance(filename, str) or not filename.strip():
        raise DriveAPIError("filename must be a non-empty string")
    data = download_drive_file(
        base_url,
        session_id,
        item_id,
        max_bytes=max_bytes,
    )
    content, encoding, total_characters, truncated = decode_text_content(
        data,
        filename=filename,
        max_characters=max_characters,
        error_type=DriveAPIError,
    )
    artifact = Artifact(
        kind="file",
        location="drive",
        reference=item_id,
        media_type=mimetypes.guess_type(filename)[0] or "text/plain",
        name=filename,
    )
    return {
        "status": "read",
        "id": item_id,
        "name": filename,
        "encoding": encoding,
        "characters": total_characters,
        "returned_characters": len(content),
        "truncated": truncated,
        "content": content,
        "artifact": artifact.tool_value(),
    }


def rename_drive_file(
    base_url: str,
    session_id: str,
    item_id: str,
    *,
    new_name: str,
    csrf_token: str | None = None,
    timeout: float = 15.0,
) -> dict[str, Any]:
    """Update a Drive file title without changing its stored bytes or type."""
    _validate_uuid(item_id, field="item_id")
    if not isinstance(new_name, str):
        raise DriveAPIError("new_name must be a string")
    clean_name = new_name.strip()
    if (
        not clean_name
        or clean_name in {".", ".."}
        or Path(clean_name).name != clean_name
        or any(character in clean_name for character in '<>:"/\\|?*')
        or clean_name.endswith((" ", "."))
    ):
        raise DriveAPIError("new_name contains invalid characters")

    try:
        with _drive_api(
            base_url, session_id, csrf_token=csrf_token
        ) as drive_api:
            current_response = drive_api.api_v1_0_items_retrieve_without_preload_content(
                UUID(item_id), _request_timeout=timeout
            )
            current = _generated_json(current_response, action="reading an item")
            if current.get("type") != "file":
                raise DriveAPIError("The selected Drive item is not a file")
            filename = current.get("filename")
            extension = Path(filename).suffix if isinstance(filename, str) else ""
            supplied_extension = Path(clean_name).suffix
            if supplied_extension:
                if extension and supplied_extension.lower() != extension.lower():
                    raise DriveAPIError(
                        "Renaming cannot change the Drive file type; keep the current extension"
                    )
                clean_name = clean_name[: -len(supplied_extension)]
            if not clean_name or len(clean_name) > 255:
                raise DriveAPIError("new_name must contain 1 to 255 characters")
            if current.get("title") == clean_name:
                raise DriveAPIError("The Drive file already has that name")

            updated_response = drive_api.api_v1_0_items_partial_update_without_preload_content(
                UUID(item_id),
                PatchedItemRequest(title=clean_name),
                _request_timeout=timeout,
                _headers=_csrf_headers(csrf_token),
            )
            updated = _generated_json(updated_response, action="renaming a file")
    except DriveAPIError as exc:
        if csrf_token is None and "HTTP 403" in str(exc):
            raise DriveAPIError(
                "Drive rejected the rename. Set DRIVE_CSRF_TOKEN to the value "
                "of your csrftoken cookie and restart the backend."
            ) from exc
        raise
    except (GeneratedDriveApiException, urllib3.exceptions.HTTPError) as exc:
        status = getattr(exc, "status", None)
        if csrf_token is None and status == 403:
            raise DriveAPIError(
                "Drive rejected the rename. Set DRIVE_CSRF_TOKEN to the value "
                "of your csrftoken cookie and restart the backend."
            ) from exc
        raise _generated_call_error(exc, action="renaming a file") from exc
    updated_filename = updated.get("filename") or filename
    media_type = updated.get("mimetype")
    if not isinstance(media_type, str):
        media_type = mimetypes.guess_type(updated_filename or "")[0] or "application/octet-stream"
    artifact = Artifact(
        kind="file",
        location="drive",
        reference=item_id,
        media_type=media_type,
        name=updated_filename or f"{clean_name}{extension}",
    )
    return {
        "status": "renamed",
        "id": item_id,
        "old_title": current.get("title"),
        "title": updated.get("title") or clean_name,
        "filename": updated_filename,
        "url_permalink": updated.get("url_permalink") or current.get("url_permalink"),
        "artifact": artifact.tool_value(),
    }


def create_drive_file(
    base_url: str,
    session_id: str,
    *,
    filename: str,
    data: bytes,
    parent_id: str | None = None,
    csrf_token: str | None = None,
    upload_acl: str | None = None,
    content_type: str = "application/octet-stream",
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Create, upload, and finalize one file in La Suite Drive."""
    _session_required(session_id)
    if parent_id is not None:
        _validate_uuid(parent_id, field="parent_id")
    try:
        with _drive_api(
            base_url, session_id, csrf_token=csrf_token
        ) as drive_api:
            if parent_id is None:
                create_response = drive_api.api_v1_0_items_create_without_preload_content(
                    CreateItemRequest(type=TypeEnum.FILE, filename=filename),
                    _request_timeout=timeout,
                    _headers=_csrf_headers(csrf_token),
                )
            else:
                create_response = drive_api.api_v1_0_items_children_create_without_preload_content(
                    UUID(parent_id),
                    ListItemRequest(title=Path(filename).stem, filename=filename),
                    _request_timeout=timeout,
                    _headers=_csrf_headers(csrf_token),
                )
            item = _generated_json(create_response, action="creating a file")
    except DriveAPIError as exc:
        if csrf_token is None and "HTTP 403" in str(exc):
            raise DriveAPIError(
                "Drive rejected file creation. Set DRIVE_CSRF_TOKEN to the value "
                "of your csrftoken cookie and restart the backend."
            ) from exc
        raise
    except (GeneratedDriveApiException, urllib3.exceptions.HTTPError) as exc:
        status = getattr(exc, "status", None)
        if csrf_token is None and status == 403:
            raise DriveAPIError(
                "Drive rejected file creation. Set DRIVE_CSRF_TOKEN to the value "
                "of your csrftoken cookie and restart the backend."
            ) from exc
        raise _generated_call_error(exc, action="creating a file") from exc

    item_id = item.get("id")
    policy = item.get("policy")
    if not isinstance(item_id, str):
        raise DriveAPIError("Drive creation response has no item id")
    _validate_uuid(item_id, field="created item id")
    if not isinstance(policy, str) or not policy:
        raise DriveAPIError("Drive creation response has no upload policy")
    parsed_policy = urlparse(policy)
    if parsed_policy.scheme not in {"http", "https"} or not parsed_policy.netloc:
        raise DriveAPIError("Drive returned an unsafe upload URL")

    upload_headers = {"Content-Type": content_type}
    if upload_acl:
        upload_headers["X-amz-acl"] = upload_acl
    upload_request = Request(
        policy, data=data, headers=upload_headers, method="PUT"
    )
    try:
        with urlopen(upload_request, timeout=timeout):
            pass
    except HTTPError as exc:
        raise DriveAPIError(
            f"Drive file storage returned HTTP {exc.code} while uploading"
        ) from exc
    except URLError as exc:
        raise DriveAPIError(
            f"Could not reach Drive file storage: {exc.reason}"
        ) from exc

    try:
        with _drive_api(
            base_url, session_id, csrf_token=csrf_token
        ) as drive_api:
            finalize_response = drive_api.api_v1_0_items_upload_ended_create_without_preload_content(
                UUID(item_id),
                ItemRequest(title=str(item.get("title") or Path(filename).stem)),
                _request_timeout=timeout,
                _headers=_csrf_headers(csrf_token),
            )
            _raise_for_generated_response(
                finalize_response, action="finalizing a file upload"
            )
            finalize_response.read()
    except (GeneratedDriveApiException, urllib3.exceptions.HTTPError) as exc:
        raise _generated_call_error(exc, action="finalizing a file upload") from exc
    artifact = Artifact(
        kind="file",
        location="drive",
        reference=item_id,
        media_type=content_type,
        name=item.get("filename") or filename,
    )
    return {
        "status": "created",
        "id": item_id,
        "title": item.get("title"),
        "filename": item.get("filename") or filename,
        "parent_id": parent_id,
        "bytes_written": len(data),
        "url_permalink": item.get("url_permalink"),
        "artifact": artifact.tool_value(),
    }
