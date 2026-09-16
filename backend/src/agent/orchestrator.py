"""Domain-agnostic reasoning loop for registered capability blocks."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any, Protocol

from agent.base import DelegationContext
from agent.blocks import BlockRegistry
from agent.errors import AgentError
from agent.events import AgentEvent
from agent.registry import AgentRegistry
from agent.selection import select_blocks
from agent.workflow_synthesizer import evaluate_workflow_suggestion
from schemas import ChatMessage


SYSTEM_PROMPT = (
    "You are the reasoning and coordination brain for La Suite Automations. The "
    "registered capabilities are the only actions and live data sources available "
    "to you. Select capabilities from their descriptions and schemas; never assume "
    "a capability exists because of prior knowledge. You may chain multiple "
    "capabilities when one result supplies the input to another. Reuse structured "
    "identifiers and paths returned by earlier calls instead of inventing them or "
    "asking the user to repeat known information. Call a capability that changes "
    "external state only when the user clearly requested that change. Never claim "
    "an action succeeded unless its result confirms success. If a result is partial "
    "or contains a limitation, state that clearly and do not present it as complete. "
    "If no registered capability can complete the request, explain the limitation "
    "and ask only for information that could make progress. Speak in user language: "
    "do not mention internal capability names, tool calls, execution steps, internal "
    "limits, or the backend."
)

STEP_LIMIT_PROMPT = (
    "Do not call another capability. Use only the results already available. Give the "
    "user the useful result gathered so far, clearly say what remains incomplete, and "
    "ask one focused question that would let the work continue. Do not mention tools, "
    "steps, internal limits, the backend, or implementation errors."
)


class ChatCompletionClient(Protocol):
    def chat_completion_stream(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> AsyncIterator[dict[str, Any]]: ...


class OrchestratorAgent:
    """Reason over advertised capabilities and coordinate their execution."""

    def __init__(
        self,
        albert: ChatCompletionClient,
        *,
        model: str,
        registry: AgentRegistry | None = None,
        block_registry: BlockRegistry | None = None,
        max_steps: int = 5,
    ) -> None:
        if registry is not None and block_registry is not None:
            raise ValueError("Provide either registry or block_registry, not both")
        self.albert = albert
        self.model = model
        self.registry = registry if registry is not None else AgentRegistry()
        self.block_registry = block_registry
        self.max_steps = max_steps

    async def run_stream(
        self, conversation: list[ChatMessage]
    ) -> AsyncIterator[AgentEvent]:
        active_registry = self.registry
        planning_prompt = SYSTEM_PROMPT
        selected_blocks: tuple[str, ...] = ()
        execution_context: list[dict[str, Any]] = []
        if self.block_registry is not None:
            selected_blocks = await select_blocks(
                self.albert,
                model=self.model,
                conversation=conversation,
                blocks=self.block_registry,
            )
            active_registry = self.block_registry.agent_registry(selected_blocks)
            planning_prompt += (
                "\n\nSelected capability manifests and known workflow routes:\n"
                + json.dumps(
                    self.block_registry.catalog(selected_blocks),
                    ensure_ascii=False,
                )
            )
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": planning_prompt},
            *(message.model_dump() for message in conversation),
        ]
        context = DelegationContext(conversation=tuple(conversation))
        used_specialist = False

        for step in range(1, self.max_steps + 1):
            yield AgentEvent("step_start", {"step": step, "max_steps": self.max_steps})

            content_parts: list[str] = []
            tool_calls: list[dict[str, Any]] = []
            async for chunk in self.albert.chat_completion_stream(
                model=self.model,
                messages=messages,
                tools=active_registry.tool_definitions(),
            ):
                if chunk["type"] == "content":
                    content_parts.append(chunk["delta"])
                    yield AgentEvent("token", {"step": step, "delta": chunk["delta"]})
                elif chunk["type"] == "done":
                    tool_calls = chunk["tool_calls"]

            content = "".join(content_parts) or None
            assistant_message: dict[str, Any] = {"role": "assistant", "content": content}
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
            messages.append(assistant_message)

            yield AgentEvent(
                "step_complete",
                {"step": step, "content": content, "tool_calls": tool_calls},
            )

            if not tool_calls:
                if not isinstance(content, str) or not content.strip():
                    raise AgentError("Albert returned an empty final answer")
                yield AgentEvent("final", {"content": content})
                async for event in self._suggest_workflow(
                    conversation, content, used_specialist
                ):
                    yield event
                return

            used_specialist = True
            for tool_call in tool_calls:
                try:
                    tool_call_id = tool_call["id"]
                    function = tool_call["function"]
                    name = function["name"]
                    arguments = function.get("arguments", "{}")
                except (KeyError, TypeError) as exc:
                    raise AgentError("Albert returned an invalid tool call") from exc

                yield AgentEvent(
                    "tool_call_start",
                    {
                        "step": step,
                        "tool_call_id": tool_call_id,
                        "name": name,
                        "arguments": arguments,
                    },
                )
                result = active_registry.dispatch(name, arguments, context)
                yield AgentEvent(
                    "tool_call_result",
                    {
                        "step": step,
                        "tool_call_id": tool_call_id,
                        "name": name,
                        "result": result,
                    },
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )
                execution_context.append({"capability": name, "result": result})

            if self.block_registry is not None and step < self.max_steps:
                next_blocks = await select_blocks(
                    self.albert,
                    model=self.model,
                    conversation=conversation,
                    blocks=self.block_registry,
                    execution_context=execution_context,
                    currently_selected=selected_blocks,
                )
                expanded_blocks = tuple(
                    dict.fromkeys((*selected_blocks, *next_blocks))
                )
                if expanded_blocks != selected_blocks:
                    selected_blocks = expanded_blocks
                    active_registry = self.block_registry.agent_registry(
                        selected_blocks
                    )
                    planning_prompt = SYSTEM_PROMPT + (
                        "\n\nSelected capability manifests and known workflow "
                        "routes:\n"
                        + json.dumps(
                            self.block_registry.catalog(selected_blocks),
                            ensure_ascii=False,
                        )
                    )
                    messages[0]["content"] = planning_prompt

        synthesis_step = self.max_steps + 1
        yield AgentEvent(
            "step_start", {"step": synthesis_step, "max_steps": self.max_steps}
        )
        messages.append({"role": "system", "content": STEP_LIMIT_PROMPT})
        content_parts = []
        async for chunk in self.albert.chat_completion_stream(
            model=self.model,
            messages=messages,
            tools=[],
        ):
            if chunk["type"] == "content":
                content_parts.append(chunk["delta"])
                yield AgentEvent(
                    "token", {"step": synthesis_step, "delta": chunk["delta"]}
                )

        content = "".join(content_parts).strip() or (
            "I could only complete part of that request. Which part would you like "
            "me to focus on next?"
        )
        yield AgentEvent(
            "step_complete",
            {"step": synthesis_step, "content": content, "tool_calls": []},
        )
        yield AgentEvent("final", {"content": content})
        async for event in self._suggest_workflow(conversation, content, used_specialist):
            yield event

    async def _suggest_workflow(
        self,
        conversation: list[ChatMessage],
        final_content: str,
        used_specialist: bool,
    ) -> AsyncIterator[AgentEvent]:
        """Best-effort: propose saving repeatable completed work as a workflow."""
        if not used_specialist:
            return
        try:
            full_conversation = [
                *conversation,
                ChatMessage(role="assistant", content=final_content),
            ]
            suggestion = await evaluate_workflow_suggestion(
                full_conversation, albert=self.albert, model=self.model
            )
        except Exception:
            return
        if suggestion.applicable:
            yield AgentEvent("workflow_suggested", suggestion.draft.model_dump())


__all__ = ["OrchestratorAgent"]
