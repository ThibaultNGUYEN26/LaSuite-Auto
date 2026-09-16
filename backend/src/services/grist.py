"""Authenticated access to the Grist REST API."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen
from uuid import uuid4

from agent.errors import GristAPIError


def _authorization_headers(api_key: str) -> dict[str, str]:
    if not api_key:
        raise GristAPIError(
            "Grist authentication is missing. Set GRIST_API_KEY and restart the backend."
        )
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


def _read_json(request: Request, *, timeout: float) -> Any:
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except HTTPError as exc:
        detail = ""
        try:
            payload = json.load(exc)
            message = payload.get("error") or payload.get("message")
            if isinstance(message, str):
                detail = f": {message}"
        except (json.JSONDecodeError, AttributeError, TypeError):
            pass
        raise GristAPIError(
            f"Grist returned HTTP {exc.code} for {request.get_method()} "
            f"{request.full_url}{detail}"
        ) from exc
    except URLError as exc:
        raise GristAPIError(
            f"Could not reach Grist at {request.full_url}: {exc.reason}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise GristAPIError("Grist returned an invalid JSON response") from exc


def list_grist_workspaces(
    base_url: str,
    api_key: str,
    *,
    org_id: str = "current",
    timeout: float = 15.0,
) -> dict[str, Any]:
    """List workspaces and their existing documents for one Grist organization."""
    clean_org_id = org_id.strip()
    if not clean_org_id:
        raise GristAPIError("org_id must not be empty")
    endpoint = urljoin(
        f"{base_url.rstrip('/')}/",
        f"api/orgs/{quote(clean_org_id, safe='')}/workspaces",
    )
    request = Request(
        endpoint,
        headers=_authorization_headers(api_key),
        method="GET",
    )
    payload = _read_json(request, timeout=timeout)
    if not isinstance(payload, list):
        raise GristAPIError("Grist workspace response is not a list")

    workspaces: list[dict[str, Any]] = []
    for workspace in payload:
        if not isinstance(workspace, dict):
            continue
        documents = workspace.get("docs")
        compact_documents = []
        if isinstance(documents, list):
            compact_documents = [
                {
                    "id": document.get("id"),
                    "name": document.get("name"),
                    "url_id": document.get("urlId"),
                }
                for document in documents
                if isinstance(document, dict)
            ]
        workspaces.append(
            {
                "id": workspace.get("id"),
                "name": workspace.get("name"),
                "access": workspace.get("access"),
                "documents": compact_documents,
            }
        )
    return {"org_id": clean_org_id, "count": len(workspaces), "workspaces": workspaces}


def _multipart_csv_body(
    *,
    boundary: str,
    filename: str,
    document_name: str,
    workspace_id: int,
    csv_data: bytes,
) -> bytes:
    separator = f"--{boundary}\r\n".encode("ascii")
    body = bytearray()

    def add_text(name: str, value: str) -> None:
        body.extend(separator)
        body.extend(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("ascii")
        )
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")

    add_text("workspaceId", str(workspace_id))
    add_text("documentName", document_name)
    body.extend(separator)
    body.extend(
        (
            f'Content-Disposition: form-data; name="upload"; filename="{filename}"\r\n'
            "Content-Type: text/csv\r\n\r\n"
        ).encode("utf-8")
    )
    body.extend(csv_data)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("ascii"))
    return bytes(body)


def import_csv_document(
    base_url: str,
    api_key: str,
    *,
    workspace_id: int,
    document_name: str,
    filename: str,
    csv_data: bytes,
    org_id: str | None = None,
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Import CSV bytes as a new saved Grist document."""
    if workspace_id <= 0:
        raise GristAPIError("workspace_id must be a positive integer")
    clean_name = document_name.strip()
    if not clean_name:
        raise GristAPIError("document_name must not be empty")
    boundary = f"grist-import-{uuid4().hex}"
    body = _multipart_csv_body(
        boundary=boundary,
        filename=filename,
        document_name=clean_name,
        workspace_id=workspace_id,
        csv_data=csv_data,
    )
    endpoint = urljoin(f"{base_url.rstrip('/')}/", "api/docs")
    headers = _authorization_headers(api_key)
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    request = Request(endpoint, data=body, headers=headers, method="POST")
    payload = _read_json(request, timeout=timeout)
    if isinstance(payload, str):
        document_id = payload
    elif isinstance(payload, dict) and isinstance(payload.get("id"), (str, int)):
        document_id = str(payload["id"])
    else:
        raise GristAPIError("Grist import response has no document id")

    document_url = None
    if org_id and org_id.strip():
        document_url = (
            f"{base_url.rstrip('/')}/o/{quote(org_id.strip(), safe='')}/doc/"
            f"{quote(document_id, safe='')}"
        )
    return {
        "status": "imported",
        "document_id": document_id,
        "document_name": clean_name,
        "workspace_id": workspace_id,
        "bytes_uploaded": len(csv_data),
        "document_url": document_url,
    }
