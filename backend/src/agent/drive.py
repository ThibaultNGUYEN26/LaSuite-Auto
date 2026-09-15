"""Drive specialist agent and its API call."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError


def get_drive_config(base_url: str, *, timeout: float = 10.0) -> dict[str, Any]:
    endpoint = urljoin(f"{base_url.rstrip('/')}/", "api/v1.0/config/")
    request = Request(endpoint, headers={"Accept": "application/json"}, method="GET")

    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise DriveAPIError(
            f"Drive returned HTTP {exc.code} for GET {endpoint}"
        ) from exc
    except URLError as exc:
        raise DriveAPIError(f"Could not reach {endpoint}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise DriveAPIError(f"Drive returned invalid JSON from {endpoint}") from exc

    if not isinstance(payload, dict):
        raise DriveAPIError(
            f"Drive returned {type(payload).__name__}; expected an object"
        )
    return payload


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
