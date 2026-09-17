"""Domain-agnostic reasoning loop for registered capability blocks."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any, Protocol
from urllib.parse import urlparse

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
    "artifacts, identifiers, and paths returned by earlier calls instead of "
    "inventing them or asking the user to repeat known information. An intermediate "
    "analysis or source artifact is not a finished file: when the user requested a "
    "deliverable, keep routing it through the capability that creates that "
    "deliverable. When the user asks about a document, including a follow-up that "
    "refers to a document discussed earlier, read that document with an available "
    "capability before answering. Treat the extracted document text as the source "
    "of truth: answer only from that text, never fill gaps with general model "
    "knowledge, and clearly say when the document does not contain the answer. "
    "Capabilities whose manifest marks them as internal are preparation steps. Call "
    "them automatically when they are needed for the user's requested outcome; the "
    "user must not have to request their cache, index, memory, or intermediate file. "
    "Do not mention an internal artifact, its format, or its path unless the user "
    "explicitly asks for implementation details. Report the useful analysis or final "
    "outcome instead. When the requested reference, subject, source, and destination "
    "can be determined from the current request, conversation, or file listing, "
    "proceed without asking the user to confirm them. Respect folders named by the "
    "user and do not silently substitute a similarly named file from elsewhere. "
    "When the user asks a factual question without knowing which PDF contains the "
    "answer, search available PDF memories first to identify likely source documents, "
    "then search those original PDFs for the passages that support the final answer. "
    "A memory is a routing guide, not final evidence. If no memory exists, search the "
    "relevant PDF collection directly instead of opening files one by one. "
    "Search with the user's core subject terms plus useful synonyms. If the first "
    "retrieval has no passage that actually answers the question, retry once with a "
    "better query before concluding that the corpus has no answer. "
    "Use the retrieved excerpts as evidence and cite them exactly as "
    "[filename, p. N]. A table of contents is only evidence about document structure, "
    "not evidence for the content of an unseen page. Never describe, recommend, or "
    "attribute information from a page that was not returned by a capability. "
    "When creating a PDF memory, use the dedicated complete-document summarization "
    "capability rather than trying to summarize a truncated read result yourself. "
    "When the user requests memories for multiple PDFs, use the bounded batch memory "
    "capability once; do not spend one orchestration step per file. "
    "When the user asks to compare exactly two local PDFs, use the dedicated PDF "
    "comparison capability. It prepares missing memories and retrieves evidence from "
    "both originals, so do not attempt to compare memory summaries by yourself. "
    "When auditing a subject represented by a folder or multiple documents, use one "
    "corpus-level audit capability that covers every in-scope evidence file. Never "
    "substitute the first file for the corpus, and do not ask permission to continue "
    "work the user already requested. "
    "A general request to analyze, understand, review, or summarize documents is not "
    "an audit. Use a descriptive corpus-analysis capability and preserve separate "
    "document summaries. Only run an audit or assign compliance verdicts when the user "
    "explicitly asks to audit, assess compliance, or compare evidence against stated "
    "requirements. When a README or manifest identifies the in-scope collection, obey "
    "that scope and do not substitute an unrelated similarly named folder. For a "
    "multi-document request, use one bounded batch/corpus capability rather than one "
    "orchestration action per document. "
    "Keep final answers clean: begin directly with the result, never expose private "
    "planning or self-talk, never say what you are about to present, and do not repeat "
    "the same introduction or completion claim. Preserve source citations returned by "
    "document capabilities. When an audit capability returns a complete criterion "
    "matrix, present the entire matrix with every criterion and column; never replace "
    "it with a shorter selection or high-level summary. Preserve the audit source "
    "register, stable source IDs, exact paths, and retrieval guidance in any saved or "
    "published report. When the user later asks about an audit finding, reopen the "
    "cited source artifact at its cited page or line range instead of relying on the "
    "report or model memory alone. When an audit request also asks for a matrix CSV "
    "or tabular destination, ask the audit capability to export its structured "
    "findings as CSV and pass the returned CSV artifact directly to a compatible "
    "destination capability; never reconstruct the audit rows from prose. If an "
    "audit capability returns a structured audit-report artifact and the user asks "
    "for a PDF, pass that artifact directly to a compatible PDF renderer. Never copy "
    "the complete audit body into another capability call or reproduce it in tool "
    "arguments. If an "
    "external write returns a URL or "
    "permalink, include it as a clickable Markdown link in the final answer, together "
    "with the local output paths. If no URL is returned, provide the resource ID and "
    "say that a direct link was unavailable rather than inventing one. "
    "PDF text uses [Page N] markers. Cite supporting PDF pages as [p. N], and do "
    "not invent a page number. If extraction is truncated, disclose that the answer "
    "only covers the pages that were available. "
    "Call a capability that changes "
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


def _append_resource_links(
    content: str, execution_context: list[dict[str, Any]]
) -> str:
    """Append verified resource URLs returned by successful capabilities."""
    links: list[tuple[str, str]] = []
    seen: set[str] = set()

    def visit(value: Any, *, key: str | None = None) -> None:
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                visit(child_value, key=child_key)
            return
        if isinstance(value, list):
            for child in value:
                visit(child, key=key)
            return
        if (
            key not in {"url_permalink", "document_url", "web_url", "url"}
            or not isinstance(value, str)
            or value in seen
            or value in content
        ):
            return
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return
        seen.add(value)
        if key == "url_permalink":
            label = "Open the uploaded report"
        elif key == "document_url":
            label = "Open the imported audit matrix"
        else:
            label = "Open the created resource"
        links.append((label, value))

    for entry in execution_context:
        visit(entry.get("result"))
    if not links:
        return content
    rendered = "\n".join(f"- [{label}]({url})" for label, url in links)
    return f"{content.rstrip()}\n\nCreated resources:\n\n{rendered}"


def _partial_result_fallback(execution_context: list[dict[str, Any]]) -> str:
    """Describe concrete completed outputs when final synthesis is empty."""
    completed: list[str] = []
    seen: set[str] = set()

    def add(value: str) -> None:
        if value not in seen:
            seen.add(value)
            completed.append(value)

    for entry in execution_context:
        result = entry.get("result")
        if not isinstance(result, dict):
            continue
        if result.get("status") == "audited":
            subject = result.get("client_directory") or result.get("client_document")
            criteria_count = result.get("criteria_count")
            source_count = result.get("source_count")
            detail = f"Audit produced for {subject or 'the selected evidence'}"
            if isinstance(criteria_count, int):
                detail += f" with {criteria_count} criteria"
            if isinstance(source_count, int):
                detail += f" across {source_count} evidence files"
            if result.get("complete") is False:
                detail += " (with reported limitations)"
            add(detail + ".")
        relative_path = result.get("relative_path")
        if isinstance(relative_path, str):
            add(f"Created `{relative_path}`.")
        audit_csv = result.get("audit_csv")
        if isinstance(audit_csv, dict) and isinstance(
            audit_csv.get("relative_path"), str
        ):
            add(f"Created `{audit_csv['relative_path']}`.")

    if not completed:
        return (
            "I could only complete part of that request, but no reusable output was "
            "confirmed. Please retry the request."
        )
    return (
        "I completed these parts:\n\n"
        + "\n".join(f"- {item}" for item in completed)
        + "\n\nSome requested publishing actions remain unfinished. You can ask me to "
        "continue them from these outputs."
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
            *(
                message.model_dump(include={"role", "content"})
                for message in conversation
            ),
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
                content = _append_resource_links(content, execution_context)
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
                result = await active_registry.dispatch_async(name, arguments, context)
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

        content = "".join(content_parts).strip() or _partial_result_fallback(
            execution_context
        )
        content = _append_resource_links(content, execution_context)
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
