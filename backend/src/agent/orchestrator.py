"""Domain-agnostic reasoning loop for registered capability blocks."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from time import perf_counter
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
    "arguments. If the dedicated audit renderer fails, report that failure; never "
    "replace it with a generic PDF creator, a script, or a previous CSV/report. If an "
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


def _is_capability_catalog_request(conversation: list[ChatMessage]) -> bool:
    """Recognize explicit requests to inspect the installed capability catalog."""
    latest_user = next(
        (
            message.content.lower()
            for message in reversed(conversation)
            if message.role == "user"
        ),
        "",
    )
    subjects = (
        "tool",
        "capabilit",
        "block",
        "bloc",
        "specialist",
        "agent available",
        "agent you have",
        "outil",
        "fonctionnalit",
    )
    catalog_actions = (
        "list",
        "show",
        "catalog",
        "available",
        "what can you do",
        "what do you have",
        "liste",
        "montre",
        "disponible",
        "qu'est-ce que tu peux",
        "que peux-tu",
    )
    return any(subject in latest_user for subject in subjects) and any(
        action in latest_user for action in catalog_actions
    )


def _render_capability_catalog(block_registry: BlockRegistry) -> str:
    """Render the live registry without asking the model to infer its contents."""
    blocks = block_registry.detailed_catalog()
    capability_count = sum(len(block["capabilities"]) for block in blocks)
    lines = [
        f"Auto currently has {len(blocks)} blocks and {capability_count} capabilities registered.",
        "",
    ]
    for block in blocks:
        lines.extend((f"## {block['name']}", "", str(block["description"])))
        permissions = block["permissions"]
        lines.extend(
            (
                "",
                "Block permissions: "
                + (", ".join(permissions) if permissions else "none declared"),
            )
        )
        required_config = block["required_config"]
        if required_config:
            config_names = [
                f"`{item['name']}`"
                + (" (required)" if item["required"] else " (optional)")
                for item in required_config
            ]
            lines.append("Configuration: " + ", ".join(config_names))

        for capability in block["capabilities"]:
            flags = []
            if capability["internal"]:
                flags.append("automatic/internal")
            if capability["confirmation_required"]:
                flags.append("confirmation required")
            suffix = f" ({', '.join(flags)})" if flags else ""
            lines.extend(
                (
                    "",
                    f"### `{capability['name']}`{suffix}",
                    "",
                    str(capability["description"]),
                    "",
                    f"- Side effect: `{capability['side_effect']}`",
                    "- Permissions: "
                    + (
                        ", ".join(capability["permissions"])
                        if capability["permissions"]
                        else "none declared"
                    ),
                    "- Accepts: "
                    + (
                        ", ".join(item["kind"] for item in capability["accepts"])
                        if capability["accepts"]
                        else "no artifact input"
                    ),
                    "- Produces: "
                    + (
                        ", ".join(item["kind"] for item in capability["produces"])
                        if capability["produces"]
                        else "no declared artifact"
                    ),
                    "- Input schema:",
                    "",
                    "```json",
                    json.dumps(capability["parameters"], ensure_ascii=False, indent=2),
                    "```",
                )
            )

        workflows = block["workflows"]
        if workflows:
            lines.extend(("", "Workflows:"))
            for workflow in workflows:
                route = " → ".join(workflow["capabilities"])
                lines.append(
                    f"- `{workflow['name']}`: {workflow['description']} ({route})"
                )
        lines.append("")
    return "\n".join(lines).rstrip()


def _requests_corpus_document_analysis(conversation: list[ChatMessage]) -> bool:
    """Detect an explicit descriptive analysis of a document collection."""
    latest_user = next(
        (
            message.content.casefold()
            for message in reversed(conversation)
            if message.role == "user"
        ),
        "",
    )
    analysis_actions = (
        "analyze",
        "analyse",
        "summarize",
        "summarise",
        "summary",
        "résume",
        "resumé",
        "résumé",
    )
    collection_terms = (
        "all documents",
        "all the documents",
        "every document",
        "documents from",
        "client folder",
        "client in",
        "folder",
        "corpus",
        "tous les documents",
        "tous les fichiers",
        "chaque document",
        "dossier",
    )
    excluded_outcomes = (
        "audit",
        "compliance",
        "conformity",
        "conformité",
        "compare",
        "comparison",
        "comparer",
    )
    negative_instruction = any(
        phrase in latest_user
        for phrase in (
            "do not",
            "don't",
            "without",
            "not yet",
            "pas encore",
            "sans audit",
            "ne compare",
        )
    )
    return (
        any(action in latest_user for action in analysis_actions)
        and any(term in latest_user for term in collection_terms)
        and (
            negative_instruction
            or not any(outcome in latest_user for outcome in excluded_outcomes)
        )
    )


def _required_outcome_instruction(capabilities: tuple[str, ...]) -> str:
    names = ", ".join(capabilities)
    return (
        "\n\nThis request explicitly covers descriptive analysis of a document "
        "collection. Complete one registered capability that produces the "
        f"document_analysis outcome before answering: {names}. Use primitive file "
        "listing or reading only to locate the collection; do not replace the "
        "bounded corpus capability with one call per file. The corpus capability "
        "performs all private document preparation automatically."
    )


def _has_completed_required_outcome(
    execution_context: list[dict[str, Any]],
    capabilities: tuple[str, ...],
) -> bool:
    """Confirm an outcome ran successfully, including declared PDF preparation."""
    for entry in execution_context:
        if entry.get("capability") not in capabilities:
            continue
        result = entry.get("result")
        if not isinstance(result, dict) or result.get("error"):
            continue
        preparation = result.get("pdf_memories")
        if not isinstance(preparation, dict):
            return True
        requested = preparation.get("requested")
        completed = sum(
            value
            for key in ("created", "updated", "skipped")
            if isinstance((value := preparation.get(key)), int)
        )
        if (
            isinstance(requested, int)
            and completed == requested
            and preparation.get("failed", 0) == 0
            and preparation.get("limited") is not True
        ):
            return True
    return False


def _successful_capabilities(
    execution_context: list[dict[str, Any]],
) -> set[str]:
    """Return capabilities whose result confirms a usable completed action."""
    completed: set[str] = set()
    failure_statuses = {"error", "failed", "rejected", "cancelled"}
    for entry in execution_context:
        capability = entry.get("capability")
        result = entry.get("result")
        if not isinstance(capability, str) or not isinstance(result, dict):
            continue
        status = str(result.get("status", "")).strip().casefold()
        if (
            result.get("error")
            or status in failure_statuses
            or result.get("complete") is False
        ):
            continue
        completed.add(capability)
    return completed


def _append_resource_links(
    content: str, execution_context: list[dict[str, Any]]
) -> str:
    """Append verified resource URLs returned by successful capabilities."""
    links: list[tuple[str, str]] = []
    seen: set[str] = set()

    def visit(
        value: Any,
        *,
        key: str | None = None,
        resource_name: str | None = None,
    ) -> None:
        if isinstance(value, dict):
            own_name = next(
                (
                    value.get(name_key)
                    for name_key in ("title", "filename", "name", "document_name")
                    if isinstance(value.get(name_key), str) and value.get(name_key)
                ),
                resource_name,
            )
            artifact = value.get("artifact")
            if isinstance(artifact, dict) and isinstance(artifact.get("name"), str):
                own_name = artifact["name"]
            for child_key, child_value in value.items():
                visit(child_value, key=child_key, resource_name=own_name)
            return
        if isinstance(value, list):
            for child in value:
                visit(child, key=key, resource_name=resource_name)
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
        label = f"Open {resource_name}" if resource_name else "Open the result"
        links.append((label, value))

    for entry in execution_context:
        result = entry.get("result")
        if not isinstance(result, dict):
            continue
        status = str(result.get("status", "")).casefold()
        if status not in {
            "created",
            "partially_created",
            "uploaded",
            "imported",
            "published",
            "updated",
            "renamed",
        }:
            continue
        visit(result)
    if not links:
        return content
    rendered = "\n".join(f"- [{label}]({url})" for label, url in links)
    return f"{content.rstrip()}\n\nCreated resources:\n\n{rendered}"


def _tool_result_for_model(result: Any) -> Any:
    """Remove redundant listing metadata before returning a result to the model."""
    if not isinstance(result, dict) or not isinstance(result.get("items"), list):
        return result

    compact = dict(result)
    compact.pop("_assistant_response", None)
    compact_items: list[Any] = []
    for item in result["items"]:
        if not isinstance(item, dict):
            compact_items.append(item)
            continue
        compact_items.append(
            {
                key: value
                for key, value in item.items()
                if key not in {"artifact", "updated_at", "url_permalink"}
                and value is not None
            }
        )
    compact["items"] = compact_items
    return compact


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
        request_started = perf_counter()
        if self.block_registry is not None and _is_capability_catalog_request(
            conversation
        ):
            content = _render_capability_catalog(self.block_registry)
            yield AgentEvent("step_start", {"step": 1, "max_steps": self.max_steps})
            yield AgentEvent("token", {"step": 1, "delta": content})
            yield AgentEvent(
                "step_complete",
                {"step": 1, "content": content, "tool_calls": []},
            )
            yield AgentEvent(
                "final",
                {
                    "content": content,
                    "total_duration_ms": round(
                        (perf_counter() - request_started) * 1000
                    ),
                },
            )
            return

        active_registry = self.registry
        planning_prompt = SYSTEM_PROMPT
        selected_blocks: tuple[str, ...] = ()
        required_capabilities: tuple[str, ...] = ()
        execution_context: list[dict[str, Any]] = []
        requires_corpus_analysis = _requests_corpus_document_analysis(conversation)
        required_outcome_capabilities: tuple[str, ...] = ()
        pending_selection_timing: dict[str, Any] | None = None
        if self.block_registry is not None:
            selection_started = perf_counter()
            selected_blocks = await select_blocks(
                self.albert,
                model=self.model,
                conversation=conversation,
                blocks=self.block_registry,
            )
            pending_selection_timing = {
                "selection_phase": "Block selection",
                "selection_duration_ms": round(
                    (perf_counter() - selection_started) * 1000
                ),
            }
            required_capabilities = selected_blocks.required_capabilities
            active_registry = self.block_registry.agent_registry(selected_blocks)
            if requires_corpus_analysis:
                required_outcome_capabilities = (
                    self.block_registry.capabilities_producing(
                        "document_analysis", selected_blocks
                    )
                )
            planning_prompt += (
                "\n\nSelected capability manifests and known workflow routes:\n"
                + json.dumps(
                    self.block_registry.catalog(selected_blocks),
                    ensure_ascii=False,
                )
            )
            if required_outcome_capabilities:
                planning_prompt += _required_outcome_instruction(
                    required_outcome_capabilities
                )
            if required_capabilities:
                planning_prompt += (
                    "\n\nThe user explicitly requested these terminal outcomes: "
                    + ", ".join(required_capabilities)
                    + ". Do not give a final answer until each has returned a "
                    "successful result. Perform private preparation and artifact "
                    "handoffs automatically."
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
            step_data: dict[str, Any] = {
                "step": step,
                "max_steps": self.max_steps,
            }
            if pending_selection_timing is not None:
                step_data.update(pending_selection_timing)
                pending_selection_timing = None
            yield AgentEvent("step_start", step_data)

            content_parts: list[str] = []
            tool_calls: list[dict[str, Any]] = []
            model_started = perf_counter()
            first_response_ms: int | None = None
            async for chunk in self.albert.chat_completion_stream(
                model=self.model,
                messages=messages,
                tools=active_registry.tool_definitions(),
            ):
                if first_response_ms is None:
                    first_response_ms = round(
                        (perf_counter() - model_started) * 1000
                    )
                if chunk["type"] == "content":
                    content_parts.append(chunk["delta"])
                    yield AgentEvent("token", {"step": step, "delta": chunk["delta"]})
                elif chunk["type"] == "done":
                    tool_calls = chunk["tool_calls"]
            model_duration_ms = round((perf_counter() - model_started) * 1000)

            content = "".join(content_parts) or None
            assistant_message: dict[str, Any] = {"role": "assistant", "content": content}
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
            messages.append(assistant_message)

            yield AgentEvent(
                "step_complete",
                {
                    "step": step,
                    "content": content,
                    "tool_calls": tool_calls,
                    "model_duration_ms": model_duration_ms,
                    "first_response_ms": first_response_ms,
                },
            )

            if not tool_calls:
                completed_capabilities = _successful_capabilities(execution_context)
                pending_capabilities = tuple(
                    capability
                    for capability in required_capabilities
                    if capability not in completed_capabilities
                )
                required_outcome_missing = (
                    required_outcome_capabilities
                    and not _has_completed_required_outcome(
                        execution_context,
                        required_outcome_capabilities,
                    )
                )
                if (required_outcome_missing or pending_capabilities) and step < self.max_steps:
                    pending_instruction = ""
                    if pending_capabilities:
                        pending_instruction = (
                            " The original request still requires these outcomes: "
                            + ", ".join(pending_capabilities)
                            + ". Call the necessary capability or capabilities now, "
                            "reusing artifacts already returned."
                        )
                    messages.append(
                        {
                            "role": "system",
                            "content": (
                                "The requested collection analysis is not complete. "
                                "Do not answer yet. Call one of the required bounded "
                                "corpus capabilities now: "
                                + ", ".join(required_outcome_capabilities)
                                + "."
                                + pending_instruction
                                if required_outcome_missing
                                else (
                                    "The original request is not complete yet."
                                    + pending_instruction
                                )
                            ),
                        }
                    )
                    continue
                if required_outcome_missing or pending_capabilities:
                    break
                if not isinstance(content, str) or not content.strip():
                    raise AgentError("Albert returned an empty final answer")
                content = _append_resource_links(content, execution_context)
                yield AgentEvent(
                    "final",
                    {
                        "content": content,
                        "total_duration_ms": round(
                            (perf_counter() - request_started) * 1000
                        ),
                    },
                )
                async for event in self._suggest_workflow(
                    conversation, content, used_specialist
                ):
                    yield event
                return

            used_specialist = True
            direct_response: str | None = None
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
                tool_started = perf_counter()
                result = await active_registry.dispatch_async(name, arguments, context)
                tool_duration_ms = round((perf_counter() - tool_started) * 1000)
                yield AgentEvent(
                    "tool_call_result",
                    {
                        "step": step,
                        "tool_call_id": tool_call_id,
                        "name": name,
                        "result": result,
                        "duration_ms": tool_duration_ms,
                    },
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(
                            _tool_result_for_model(result), ensure_ascii=False
                        ),
                    }
                )
                execution_context.append({"capability": name, "result": result})
                candidate_response = (
                    result.get("_assistant_response")
                    if isinstance(result, dict)
                    else None
                )
                if isinstance(candidate_response, str) and candidate_response.strip():
                    direct_response = candidate_response

            completed_capabilities = _successful_capabilities(execution_context)
            pending_capabilities = tuple(
                capability
                for capability in required_capabilities
                if capability not in completed_capabilities
            )
            required_outcome_missing = (
                required_outcome_capabilities
                and not _has_completed_required_outcome(
                    execution_context,
                    required_outcome_capabilities,
                )
            )
            if (
                direct_response is not None
                and len(tool_calls) == 1
                and not pending_capabilities
                and not required_outcome_missing
            ):
                content = _append_resource_links(direct_response, execution_context)
                yield AgentEvent(
                    "final",
                    {
                        "content": content,
                        "total_duration_ms": round(
                            (perf_counter() - request_started) * 1000
                        ),
                    },
                )
                async for event in self._suggest_workflow(
                    conversation, content, used_specialist
                ):
                    yield event
                return

            result_can_enable_another_block = any(
                isinstance(entry.get("result"), dict)
                and any(
                    key in entry["result"]
                    for key in ("artifact", "artifacts", "audit_csv", "report_artifact")
                )
                for entry in execution_context[-len(tool_calls) :]
            )
            available_capabilities = {
                tool["function"]["name"]
                for tool in active_registry.tool_definitions()
            }
            pending_capability_is_unavailable = any(
                capability not in available_capabilities
                for capability in pending_capabilities
            )
            if (
                self.block_registry is not None
                and step < self.max_steps
                and result_can_enable_another_block
                and (
                    not required_capabilities
                    or pending_capability_is_unavailable
                )
            ):
                selection_started = perf_counter()
                next_blocks = await select_blocks(
                    self.albert,
                    model=self.model,
                    conversation=conversation,
                    blocks=self.block_registry,
                    execution_context=execution_context,
                    currently_selected=selected_blocks,
                )
                pending_selection_timing = {
                    "selection_phase": "Block reconsideration",
                    "selection_duration_ms": round(
                        (perf_counter() - selection_started) * 1000
                    ),
                }
                required_capabilities = tuple(
                    dict.fromkeys(
                        (
                            *required_capabilities,
                            *next_blocks.required_capabilities,
                        )
                    )
                )
                expanded_blocks = tuple(
                    dict.fromkeys((*selected_blocks, *next_blocks))
                )
                if expanded_blocks != selected_blocks:
                    selected_blocks = expanded_blocks
                    active_registry = self.block_registry.agent_registry(
                        selected_blocks
                    )
                    if requires_corpus_analysis:
                        required_outcome_capabilities = (
                            self.block_registry.capabilities_producing(
                                "document_analysis", selected_blocks
                            )
                        )
                    planning_prompt = SYSTEM_PROMPT + (
                        "\n\nSelected capability manifests and known workflow "
                        "routes:\n"
                        + json.dumps(
                            self.block_registry.catalog(selected_blocks),
                            ensure_ascii=False,
                        )
                    )
                    if required_outcome_capabilities:
                        planning_prompt += _required_outcome_instruction(
                            required_outcome_capabilities
                        )
                    if required_capabilities:
                        planning_prompt += (
                            "\n\nThe user explicitly requested these terminal outcomes: "
                            + ", ".join(required_capabilities)
                            + ". Do not give a final answer until each has returned a "
                            "successful result. Perform private preparation and "
                            "artifact handoffs automatically."
                        )
                    messages[0]["content"] = planning_prompt

        synthesis_step = self.max_steps + 1
        synthesis_data: dict[str, Any] = {
            "step": synthesis_step,
            "max_steps": self.max_steps,
        }
        if pending_selection_timing is not None:
            synthesis_data.update(pending_selection_timing)
        yield AgentEvent("step_start", synthesis_data)
        messages.append({"role": "system", "content": STEP_LIMIT_PROMPT})
        content_parts = []
        model_started = perf_counter()
        first_response_ms = None
        async for chunk in self.albert.chat_completion_stream(
            model=self.model,
            messages=messages,
            tools=[],
        ):
            if first_response_ms is None:
                first_response_ms = round((perf_counter() - model_started) * 1000)
            if chunk["type"] == "content":
                content_parts.append(chunk["delta"])
                yield AgentEvent(
                    "token", {"step": synthesis_step, "delta": chunk["delta"]}
                )
        model_duration_ms = round((perf_counter() - model_started) * 1000)

        content = "".join(content_parts).strip() or _partial_result_fallback(
            execution_context
        )
        content = _append_resource_links(content, execution_context)
        yield AgentEvent(
            "step_complete",
            {
                "step": synthesis_step,
                "content": content,
                "tool_calls": [],
                "model_duration_ms": model_duration_ms,
                "first_response_ms": first_response_ms,
            },
        )
        yield AgentEvent(
            "final",
            {
                "content": content,
                "total_duration_ms": round(
                    (perf_counter() - request_started) * 1000
                ),
            },
        )
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
