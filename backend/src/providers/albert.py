"""Client for Albert's OpenAI-compatible API."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import httpx

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

    async def chat_completion_stream(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream one chat completion, yielding content deltas as they arrive.

        Yields ``{"type": "content", "delta": str}`` for each content
        fragment, followed by exactly one
        ``{"type": "done", "tool_calls": list[dict]}`` once the stream ends,
        with any streamed tool-call fragments reassembled by index.
        """
        endpoint = urljoin(f"{self.base_url}/", "chat/completions")
        headers = {
            "Accept": "text/event-stream",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "temperature": 0.2,
            "stream": True,
        }

        tool_call_fragments: dict[int, dict[str, Any]] = {}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST", endpoint, headers=headers, json=payload
                ) as response:
                    if response.status_code >= 400:
                        body = await response.aread()
                        raise AlbertAPIError(
                            f"Albert returned HTTP {response.status_code} for "
                            f"POST {endpoint}: {body.decode(errors='replace')}"
                        )
                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        data = line[len("data:") :].strip()
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                        except json.JSONDecodeError as exc:
                            raise AlbertAPIError(
                                "Albert returned an invalid stream chunk"
                            ) from exc
                        try:
                            delta = chunk["choices"][0]["delta"]
                        except (KeyError, IndexError, TypeError):
                            continue
                        content = delta.get("content")
                        if content:
                            yield {"type": "content", "delta": content}
                        for fragment in delta.get("tool_calls") or []:
                            index = fragment.get("index", 0)
                            entry = tool_call_fragments.setdefault(
                                index,
                                {
                                    "id": None,
                                    "type": "function",
                                    "function": {"name": "", "arguments": ""},
                                },
                            )
                            if fragment.get("id"):
                                entry["id"] = fragment["id"]
                            function_fragment = fragment.get("function") or {}
                            if function_fragment.get("name"):
                                entry["function"]["name"] += function_fragment["name"]
                            if function_fragment.get("arguments"):
                                entry["function"]["arguments"] += function_fragment[
                                    "arguments"
                                ]
        except httpx.HTTPError as exc:
            raise AlbertAPIError(f"Could not reach {endpoint}: {exc}") from exc

        tool_calls = [tool_call_fragments[i] for i in sorted(tool_call_fragments)]
        yield {"type": "done", "tool_calls": tool_calls}
