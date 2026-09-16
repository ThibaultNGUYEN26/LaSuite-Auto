"""First-stage selection of relevant capability blocks."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any, Protocol

from agent.blocks import BlockRegistry
from agent.errors import AgentError
from schemas import ChatMessage


SELECTION_FUNCTION = "select_capability_blocks"


class SelectionClient(Protocol):
    def chat_completion_stream(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        tool_choice: str | dict[str, Any] = "auto",
    ) -> AsyncIterator[dict[str, Any]]: ...


async def select_blocks(
    client: SelectionClient,
    *,
    model: str,
    conversation: list[ChatMessage],
    blocks: BlockRegistry,
    execution_context: list[dict[str, Any]] | None = None,
    currently_selected: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Choose blocks from compact manifests before exposing detailed tool schemas.

    The selector may be called again after a capability has run. This lets the
    orchestrator discover the next block from a produced artifact without making
    every installed tool visible to the planning model.
    """
    if not blocks.names:
        return ()
    catalog = blocks.catalog()
    tools = [
        {
            "type": "function",
            "function": {
                "name": SELECTION_FUNCTION,
                "description": (
                    "Select every capability block that may be needed to answer the "
                    "user's request. Select none for a purely conversational answer."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "blocks": {
                            "type": "array",
                            "items": {"type": "string", "enum": list(blocks.names)},
                            "uniqueItems": True,
                        }
                    },
                    "required": ["blocks"],
                    "additionalProperties": False,
                },
            },
        }
    ]
    selection_instructions = (
        "You select relevant capability blocks for another reasoning agent. "
        "Choose all blocks that may participate in the request, including "
        "sources, transformations, and destinations in a multi-step task. "
        "When execution progress is supplied, choose every block that may still "
        "be needed to finish the original request. Do not execute the task. "
        "Here is the compact block catalog:\n"
        + json.dumps(catalog, ensure_ascii=False)
    )
    if currently_selected:
        selection_instructions += (
            "\nBlocks already available to the reasoning agent: "
            + json.dumps(currently_selected, ensure_ascii=False)
        )

    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": selection_instructions,
        },
        *(message.model_dump() for message in conversation),
    ]
    if execution_context:
        progress = json.dumps(execution_context[-8:], ensure_ascii=False)
        if len(progress) > 12_000:
            progress = progress[:12_000] + "…"
        messages.append(
            {
                "role": "system",
                "content": (
                    "Execution progress from the current request follows. Use it "
                    "to identify the blocks needed for the remaining work:\n"
                    + progress
                ),
            }
        )
    tool_calls: list[dict[str, Any]] = []
    async for chunk in client.chat_completion_stream(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": SELECTION_FUNCTION}},
    ):
        if chunk.get("type") == "done":
            tool_calls = chunk.get("tool_calls") or []

    for tool_call in tool_calls:
        function = tool_call.get("function") or {}
        if function.get("name") != SELECTION_FUNCTION:
            continue
        try:
            arguments = json.loads(function.get("arguments") or "{}")
            selected = arguments["blocks"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise AgentError("The capability selector returned invalid data") from exc
        if not isinstance(selected, list) or not all(
            isinstance(name, str) for name in selected
        ):
            raise AgentError("The capability selector returned invalid block names")
        unknown = sorted(set(selected) - set(blocks.names))
        if unknown:
            raise AgentError(
                f"The capability selector returned unknown blocks: {', '.join(unknown)}"
            )
        return tuple(dict.fromkeys(selected))
    raise AgentError("The capability selector did not choose any block set")
