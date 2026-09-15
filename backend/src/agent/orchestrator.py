"""Coordinator that routes model tool calls to registered specialist agents."""

from __future__ import annotations

import json
from typing import Any, Protocol

from agent.base import DelegationContext
from agent.drive import DriveConfigAgent, DriveListItemsAgent, get_drive_config
from agent.errors import AgentError, AlbertAPIError, DriveAPIError
from agent.registry import AgentRegistry
from config import settings
from providers.albert import AlbertClient
from providers.echo import EchoProvider
from schemas import ChatMessage


SYSTEM_PROMPT = (
    "You are the coordinator for La Suite Automations. Route tasks to the most "
    "appropriate registered specialist agent whenever current data or an action "
    "is required. You may call multiple agents in sequence. Do not claim an action "
    "succeeded unless its agent result confirms it. If no available agent can do "
    "the work, explain that limitation instead of guessing."
)


class ChatCompletionClient(Protocol):
    def chat_completion(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> dict[str, Any]: ...


class OrchestratorAgent:
    """Run the coordinator loop and dispatch calls through an agent registry."""

    def __init__(
        self,
        albert: ChatCompletionClient,
        *,
        model: str,
        registry: AgentRegistry | None = None,
        drive_base_url: str | None = None,
        max_steps: int = 5,
    ) -> None:
        # ``drive_base_url`` keeps the original constructor compatible while
        # callers migrate to explicit registry composition.
        if registry is None:
            if drive_base_url is None:
                raise ValueError("Provide an agent registry or drive_base_url")
            registry = AgentRegistry([DriveConfigAgent(drive_base_url)])
        self.albert = albert
        self.model = model
        self.registry = registry
        self.max_steps = max_steps

    def run(self, conversation: list[ChatMessage]) -> str:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *(message.model_dump() for message in conversation),
        ]
        context = DelegationContext(conversation=tuple(conversation))

        for _ in range(self.max_steps):
            assistant_message = self.albert.chat_completion(
                model=self.model,
                messages=messages,
                tools=self.registry.tool_definitions(),
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
                result = self.registry.dispatch(name, arguments, context)
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


def build_agent_registry() -> AgentRegistry:
    """Composition root: register every specialist available to the coordinator."""
    return AgentRegistry(
        [
            DriveConfigAgent(settings.drive_base_url),
            DriveListItemsAgent(
                settings.drive_base_url,
                settings.drive_session_id,
            ),
        ]
    )


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
        registry=build_agent_registry(),
    )
    return _albert_agent


def run(messages: list[ChatMessage]) -> str:
    if settings.provider == "echo":
        return _echo_provider.generate(messages)
    if settings.provider == "albert":
        return _get_albert_agent().run(messages)
    raise AgentError(f"Unknown AUTO_PROVIDER: {settings.provider}")


# Preserve imports used by existing callers while implementation lives in
# focused modules.
__all__ = [
    "AgentError",
    "AlbertAPIError",
    "AlbertClient",
    "DriveAPIError",
    "OrchestratorAgent",
    "build_agent_registry",
    "get_drive_config",
    "run",
]
