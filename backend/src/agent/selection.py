"""First-stage selection of relevant capability blocks."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any, Protocol

from agent.blocks import BlockRegistry
from schemas import ChatMessage


SELECTION_FUNCTION = "select_capability_blocks"


def _validated_selection(
    value: Any, available: tuple[str, ...]
) -> tuple[str, ...] | None:
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list) or not all(
        isinstance(name, str) for name in value
    ):
        return None
    available_names = set(available)
    if any(name not in available_names for name in value):
        return None
    return tuple(dict.fromkeys(value))


def _selection_from_text(
    content: str, available: tuple[str, ...]
) -> tuple[str, ...] | None:
    clean = content.strip()
    if not clean:
        return None
    if clean.startswith("```") and clean.endswith("```"):
        lines = clean.splitlines()
        clean = "\n".join(lines[1:-1]).strip()
    try:
        payload = json.loads(clean)
    except json.JSONDecodeError:
        mentioned = [name for name in available if name in clean]
        return tuple(mentioned) if mentioned else None
    if isinstance(payload, dict):
        payload = payload.get("blocks")
    return _validated_selection(payload, available)


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
        "Understand the user's intended outcome in any language; the user does "
        "not need to name a block, integration, filename, or technical action. "
        "Choose all blocks that may participate in the request, including "
        "sources, transformations, and destinations in a multi-step task. "
        "Prefer purpose-built blocks over general code execution whenever a "
        "dedicated capability covers the requested outcome. "
        "A capability marked internal is an automatic preparation step, not something "
        "the user must name. Select its block whenever that preparation is needed. "
        "For a request to analyze, review, understand, or audit a complete document, "
        "select the document's source block so its internal preparation can run. "
        "For an audit of a folder, client, or multi-document corpus, select the source "
        "block that advertises corpus-level auditing rather than treating one file as "
        "the complete subject. "
        "Do not interpret general analysis, review, understanding, or summarization as "
        "an audit unless the user explicitly requests compliance verdicts or comparison "
        "against requirements. Prefer a bounded corpus-analysis capability when several "
        "documents must be processed. "
        "For analysis, trends, evolution, comparisons, or change over time, "
        "select a matching analysis block. When the data location is stated or "
        "existing files must be discovered, also select the relevant source block. "
        "For a follow-up question about a file or document discussed earlier, "
        "select its source block again so the reasoning agent can reopen it; do not "
        "treat that question as purely conversational. Use the full conversation to "
        "resolve references such as 'it', 'this file', or 'the PDF'. "
        "When the user asks a question that could be answered by searching a set of "
        "PDFs, select the relevant file-source blocks even if no filename is given. "
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
            progress = progress[:12_000] + "..."
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
    content_parts: list[str] = []
    async for chunk in client.chat_completion_stream(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": SELECTION_FUNCTION}},
    ):
        if chunk.get("type") == "content" and isinstance(chunk.get("delta"), str):
            content_parts.append(chunk["delta"])
        elif chunk.get("type") == "done":
            tool_calls = chunk.get("tool_calls") or []

    for tool_call in tool_calls:
        function = tool_call.get("function") or {}
        if function.get("name") != SELECTION_FUNCTION:
            continue
        try:
            arguments = json.loads(function.get("arguments") or "{}")
        except (json.JSONDecodeError, TypeError):
            continue
        selected = _validated_selection(arguments.get("blocks"), blocks.names)
        if selected is not None:
            return selected

    selected = _selection_from_text("".join(content_parts), blocks.names)
    if selected is not None:
        return selected

    retry_messages = [
        *messages,
        {
            "role": "system",
            "content": (
                "The previous selection response was missing or malformed. Return "
                "only JSON in this exact form: {\"blocks\": [\"block_name\"]}. "
                "Use only names from the catalog. An empty list is valid only when "
                "the request needs no capability."
            ),
        },
    ]
    retry_content: list[str] = []
    async for chunk in client.chat_completion_stream(
        model=model,
        messages=retry_messages,
        tools=[],
        tool_choice="auto",
    ):
        if chunk.get("type") == "content" and isinstance(chunk.get("delta"), str):
            retry_content.append(chunk["delta"])
    selected = _selection_from_text("".join(retry_content), blocks.names)
    if selected is not None:
        return selected

    # Selector formatting failures must not become user-visible backend errors.
    # With no new tools, the planner can ask the user where the data is located.
    return currently_selected
