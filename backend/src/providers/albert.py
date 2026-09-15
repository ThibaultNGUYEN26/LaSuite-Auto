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
            detail = ""
            try:
                error_payload = json.load(exc)
                error_detail = error_payload.get("detail")
                if isinstance(error_detail, str):
                    detail = f": {error_detail}"
                elif isinstance(error_detail, list):
                    messages = [
                        str(item.get("msg"))
                        for item in error_detail
                        if isinstance(item, dict) and item.get("msg")
                    ]
                    if messages:
                        detail = f": {'; '.join(messages)}"
                if not detail and isinstance(error_payload.get("message"), str):
                    detail = f": {error_payload['message']}"
                error_object = error_payload.get("error")
                if not detail and isinstance(error_object, dict):
                    error_message = error_object.get("message")
                    if isinstance(error_message, str):
                        detail = f": {error_message}"
                errors = error_payload.get("errors")
                if not detail and isinstance(errors, list):
                    messages = [
                        str(item.get("detail") or item.get("msg"))
                        for item in errors
                        if isinstance(item, dict) and (item.get("detail") or item.get("msg"))
                    ]
                    if messages:
                        detail = f": {'; '.join(messages)}"
            except (json.JSONDecodeError, AttributeError, TypeError):
                pass
            raise AlbertAPIError(
                f"Albert returned HTTP {exc.code} for {method} {endpoint}{detail}"
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

    def resolve_model_by_type(
        self,
        model_type: str,
        requested_model: str | None = None,
        *,
        setting_name: str = "ALBERT_MODEL",
    ) -> str:
        payload = self._request("models")
        models = payload.get("data")
        if not isinstance(models, list):
            raise AlbertAPIError("Albert's model catalogue has no data list")

        model_ids = [
            model.get("id")
            for model in models
            if isinstance(model, dict)
            and model.get("type") == model_type
            and isinstance(model.get("id"), str)
        ]
        if requested_model is not None:
            if requested_model not in model_ids:
                raise AlbertAPIError(
                    f"{setting_name} must be a canonical {model_type} model id; "
                    f"available ids: {', '.join(model_ids) or 'none'}"
                )
            return requested_model
        if not model_ids:
            raise AlbertAPIError(f"Albert currently exposes no {model_type} model")
        return model_ids[0]

    def resolve_model(self, requested_model: str | None = None) -> str:
        return self.resolve_model_by_type("text-generation", requested_model)

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

    def image_completion(
        self,
        *,
        model: str,
        prompt: str,
        data_url: str,
    ) -> str:
        payload = self._request(
            "chat/completions",
            body={
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": data_url}},
                        ],
                    }
                ],
                "temperature": 0.2,
            },
        )
        try:
            content = payload["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise AlbertAPIError("Albert returned no image analysis") from exc
        if not isinstance(content, str) or not content.strip():
            raise AlbertAPIError("Albert returned an empty image analysis")
        return content
