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
