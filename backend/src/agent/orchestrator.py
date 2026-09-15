"""Agent loop that lets Albert call tools backed by La Suite APIs."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from config import settings
from providers.echo import EchoProvider
from schemas import ChatMessage


SYSTEM_PROMPT = (
    "You are an assistant for La Suite. Use the available tools whenever the "
    "user's request requires current information from La Suite services. "
    "Explain tool results clearly and never claim that a tool ran when it did not."
)

TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "drive_get_config",
            "description": (
                "Get the current public configuration of the La Suite Drive "
                "instance, including languages, feature flags, and public URLs."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    }
]


class AgentError(RuntimeError):
    """Raised when the agent cannot complete a request."""


class DriveAPIError(AgentError):
    """Raised when Drive cannot return a usable response."""


class AlbertAPIError(AgentError):
    """Raised when Albert cannot return a usable response."""


def _decode_json_response(request: Request, *, timeout: float) -> dict[str, Any]:
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise AgentError(
            f"{request.host} returned HTTP {exc.code} for {request.get_method()} "
            f"{request.full_url}"
        ) from exc
    except URLError as exc:
        raise AgentError(f"Could not reach {request.full_url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise AgentError(f"Invalid JSON returned by {request.full_url}") from exc

    if not isinstance(payload, dict):
        raise AgentError(
            f"{request.full_url} returned {type(payload).__name__}; expected an object"
        )
    return payload


def get_drive_config(base_url: str, *, timeout: float = 10.0) -> dict[str, Any]:
    """Call Drive's public ``GET /api/v1.0/config/`` endpoint."""
    endpoint = urljoin(f"{base_url.rstrip('/')}/", "api/v1.0/config/")
    request = Request(endpoint, headers={"Accept": "application/json"}, method="GET")

    try:
        return _decode_json_response(request, timeout=timeout)
    except AgentError as exc:
        raise DriveAPIError(str(exc)) from exc


class AlbertClient:
    """Small client for Albert's OpenAI-compatible API endpoints."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str,
        timeout: float = 60.0,
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
            return _decode_json_response(request, timeout=self.timeout)
        except AgentError as exc:
            raise AlbertAPIError(str(exc)) from exc

    def resolve_model(self, requested_model: str | None = None) -> str:
        """Return a live canonical ID for a text-generation model."""
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
        """Request one non-streaming chat-completion turn."""
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


class OrchestratorAgent:
    """Run the Albert/tool loop for a conversation."""

    def __init__(
        self,
        albert: AlbertClient,
        *,
        model: str,
        drive_base_url: str,
        max_steps: int = 5,
    ) -> None:
        self.albert = albert
        self.model = model
        self.drive_base_url = drive_base_url
        self.max_steps = max_steps

    def _run_tool(self, name: str, arguments: str) -> dict[str, Any]:
        try:
            parsed_arguments = json.loads(arguments or "{}")
        except json.JSONDecodeError as exc:
            return {"error": f"Invalid tool arguments: {exc.msg}"}
        if not isinstance(parsed_arguments, dict):
            return {"error": "Tool arguments must be a JSON object"}
        if name == "drive_get_config":
            if parsed_arguments:
                return {"error": "drive_get_config does not accept arguments"}
            try:
                return get_drive_config(self.drive_base_url)
            except DriveAPIError as exc:
                return {"error": str(exc)}
        return {"error": f"Unknown tool: {name}"}

    def run(self, conversation: list[ChatMessage]) -> str:
        """Answer a conversation, allowing Albert to call tools as needed."""
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *(message.model_dump() for message in conversation),
        ]

        for _ in range(self.max_steps):
            assistant_message = self.albert.chat_completion(
                model=self.model,
                messages=messages,
                tools=TOOLS,
            )
            messages.append(assistant_message)
            tool_calls = assistant_message.get("tool_calls") or []
            if not tool_calls:
                content = assistant_message.get("content")
                if not isinstance(content, str) or not content.strip():
                    raise AgentError("Albert returned an empty final answer")
                return content

            for tool_call in tool_calls:
                try:
                    tool_call_id = tool_call["id"]
                    function = tool_call["function"]
                    name = function["name"]
                    arguments = function.get("arguments", "{}")
                except (KeyError, TypeError) as exc:
                    raise AgentError("Albert returned an invalid tool call") from exc
                result = self._run_tool(name, arguments)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )

        raise AgentError(f"Agent exceeded its {self.max_steps}-step limit")


_echo_provider = EchoProvider()
_albert_agent: OrchestratorAgent | None = None


def _get_albert_agent() -> OrchestratorAgent:
    global _albert_agent
    if _albert_agent is not None:
        return _albert_agent
    if not settings.albert_api_key:
        raise AgentError("Set ALBERT_API_KEY before using the Albert provider")

    albert = AlbertClient(
        settings.albert_api_key,
        base_url=settings.albert_base_url,
    )
    model = albert.resolve_model(settings.albert_model)
    _albert_agent = OrchestratorAgent(
        albert,
        model=model,
        drive_base_url=settings.drive_base_url,
    )
    return _albert_agent


def run(messages: list[ChatMessage]) -> str:
    """Run a conversation through the configured backend provider."""
    if settings.provider == "echo":
        return _echo_provider.generate(messages)
    if settings.provider == "albert":
        return _get_albert_agent().run(messages)
    raise AgentError(f"Unknown AUTO_PROVIDER: {settings.provider}")
