"""Client for Albert's OpenAI-compatible API."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from agent.errors import AlbertAPIError


class AlbertClient:
    def __init__(
        self, api_key: str, *, base_url: str, timeout: float = 60.0
    ) -> None:
        if not api_key:
            raise ValueError("An Albert API key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(
        self, path: str, *, body: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        endpoint = urljoin(f"{self.base_url}/", path.lstrip("/"))
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = None
        method = "GET"
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body).encode("utf-8")
            method = "POST"
        request = Request(endpoint, data=data, headers=headers, method=method)

        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = json.load(response)
        except HTTPError as exc:
            raise AlbertAPIError(
                f"Albert returned HTTP {exc.code} for {method} {endpoint}"
            ) from exc
        except URLError as exc:
            raise AlbertAPIError(f"Could not reach {endpoint}: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise AlbertAPIError(f"Albert returned invalid JSON from {endpoint}") from exc

        if not isinstance(payload, dict):
            raise AlbertAPIError(
                f"Albert returned {type(payload).__name__}; expected an object"
            )
        return payload

    def resolve_model(self, requested_model: str | None = None) -> str:
        payload = self._request("models")
        models = payload.get("data")
        if not isinstance(models, list):
            raise AlbertAPIError("Albert's model catalogue has no data list")

        model_ids = [
            model.get("id")
            for model in models
            if isinstance(model, dict)
            and model.get("type") == "text-generation"
            and isinstance(model.get("id"), str)
        ]
        if requested_model is not None:
            if requested_model not in model_ids:
                raise AlbertAPIError(
                    "ALBERT_MODEL must be a canonical text-generation model id; "
                    f"available ids: {', '.join(model_ids) or 'none'}"
                )
            return requested_model
        if not model_ids:
            raise AlbertAPIError("Albert currently exposes no text-generation model")
        return model_ids[0]

    def chat_completion(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> dict[str, Any]:
        payload = self._request(
            "chat/completions",
            body={
                "model": model,
                "messages": messages,
                "tools": tools,
                "tool_choice": "auto",
                "temperature": 0.2,
            },
        )
        try:
            message = payload["choices"][0]["message"]
        except (KeyError, IndexError, TypeError) as exc:
            raise AlbertAPIError("Albert returned no assistant message") from exc
        if not isinstance(message, dict):
            raise AlbertAPIError("Albert returned an invalid assistant message")
        return message
