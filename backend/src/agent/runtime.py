"""Application composition for providers, blocks, and the orchestrator."""

from __future__ import annotations

from collections.abc import AsyncIterator

from agent.blocks import BlockRegistry
from agent.errors import AgentError
from agent.events import AgentEvent
from agent.orchestrator import OrchestratorAgent
from agent.workflow_synthesizer import evaluate_workflow_suggestion
from config import settings
from providers.albert import AlbertClient
from providers.echo import EchoProvider
from schemas import ChatMessage, WorkflowDraft
from services.chat_title import fallback_title, generate_title


_echo_provider = EchoProvider()
_albert_client: AlbertClient | None = None
_resolved_albert_model: str | None = None
_albert_agent: OrchestratorAgent | None = None


def _get_albert_client() -> tuple[AlbertClient, str]:
    global _albert_client, _resolved_albert_model
    if _albert_client is not None and _resolved_albert_model is not None:
        return _albert_client, _resolved_albert_model
    if not settings.albert_api_key:
        raise AgentError("Set ALBERT_API_KEY before using the Albert provider")

    _albert_client = AlbertClient(
        settings.albert_api_key,
        base_url=settings.albert_base_url,
    )
    _resolved_albert_model = _albert_client.resolve_model(settings.albert_model)
    return _albert_client, _resolved_albert_model


def _get_albert_agent() -> OrchestratorAgent:
    global _albert_agent
    if _albert_agent is not None:
        return _albert_agent
    albert, model = _get_albert_client()
    _albert_agent = OrchestratorAgent(
        albert,
        model=model,
        max_steps=settings.orchestrator_max_steps,
        block_registry=BlockRegistry.discover(
            allowed_permissions=settings.block_allowed_permissions
        ),
    )
    return _albert_agent


async def run_stream(messages: list[ChatMessage]) -> AsyncIterator[AgentEvent]:
    if settings.provider == "echo":
        yield AgentEvent("final", {"content": _echo_provider.generate(messages)})
        return
    if settings.provider == "albert":
        async for event in _get_albert_agent().run_stream(messages):
            yield event
        return
    raise AgentError(f"Unknown AUTO_PROVIDER: {settings.provider}")


async def draft_workflow_from_messages(messages: list[ChatMessage]) -> WorkflowDraft:
    """Generalize a conversation into a reusable workflow draft."""
    if settings.provider == "albert" and settings.albert_api_key:
        agent = _get_albert_agent()
        suggestion = await evaluate_workflow_suggestion(
            messages, albert=agent.albert, model=agent.model
        )
    else:
        suggestion = await evaluate_workflow_suggestion(
            messages, albert=None, model=None
        )
    return suggestion.draft


async def generate_chat_title(prompt: str, response: str) -> str:
    """Create a short title without involving capability selection or tools."""
    if settings.provider == "echo":
        return fallback_title(prompt)
    if settings.provider == "albert":
        albert, model = _get_albert_client()
        return await generate_title(
            prompt,
            response,
            albert=albert,
            model=model,
        )
    raise AgentError(f"Unknown AUTO_PROVIDER: {settings.provider}")


async def close_runtime() -> None:
    """Release persistent provider connections during application shutdown."""
    await AlbertClient.close_all()
