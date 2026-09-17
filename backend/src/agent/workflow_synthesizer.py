"""Judges whether a conversation is workflow-worthy and generalizes it."""

from __future__ import annotations

import json
from typing import Any, Protocol

from agent.errors import AgentError
from schemas import ChatMessage, WorkflowDraft

SUGGESTION_SYSTEM_PROMPT = (
    "You judge whether a finished chat conversation is worth saving as a "
    "reusable workflow, and if so, generalize it.\n\n"
    "A conversation is applicable only when the assistant carried out a "
    "concrete action against a specific target — a file, a folder, a Drive "
    "item — using its tools, AND that same action would make sense to repeat "
    "later against a different target (e.g. 'summarize this PDF', 'extract "
    "emails from these invoices', 'list files modified this week in this "
    "folder'). A conversation is NOT applicable when it was purely "
    "conversational or exploratory, a one-off question with no repeatable "
    "target, a request that failed or was only partially completed, or a "
    "clarifying back-and-forth rather than a finished action.\n\n"
    "Respond with ONLY a JSON object with exactly these keys: "
    "applicable (boolean), name, description, instructions, input_question. "
    "Always fill in name (a short title, a few words), description (one "
    "line), instructions (the reusable task with the specific file/folder/"
    "item replaced by a placeholder for future input), and input_question "
    "(what to ask the user the next time this workflow runs) as your best "
    "generalization of the conversation, regardless of the applicable "
    "verdict — applicable only signals whether this conversation is a good "
    "candidate to proactively suggest saving, not whether the other fields "
    "should be filled in. No markdown, no extra text before or after the "
    "JSON."
)


class DraftChatClient(Protocol):
    def chat_completion_stream(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ): ...


class WorkflowSuggestion:
    """The model's verdict on a conversation, plus its draft if applicable."""

    def __init__(self, applicable: bool, draft: WorkflowDraft) -> None:
        self.applicable = applicable
        self.draft = draft


def _fallback_suggestion(messages: list[ChatMessage]) -> WorkflowSuggestion:
    """Best-effort draft when no LLM is available (e.g. the echo provider).

    There is no way to judge applicability without a model, so this always
    reports ``applicable=True``; callers that care about the judgement (the
    proactive suggestion path) only reach here when a specialist tool was
    already used, which is itself a reasonable signal in that fallback case.
    """
    first_user = next((m.content for m in messages if m.role == "user"), "").strip()
    title = (first_user.splitlines() or [""])[0][:60] or "Untitled workflow"
    return WorkflowSuggestion(
        applicable=True,
        draft=WorkflowDraft(
            name=title,
            description=title,
            instructions=first_user or "Repeat the previous task.",
            input_question="Which file or folder should I run this on?",
        ),
    )


def _parse_suggestion(raw: str) -> WorkflowSuggestion:
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise AgentError("Could not evaluate this conversation as a workflow")
    try:
        payload = json.loads(raw[start : end + 1])
    except json.JSONDecodeError as exc:
        raise AgentError("Could not evaluate this conversation as a workflow") from exc

    if not isinstance(payload, dict) or "applicable" not in payload:
        raise AgentError("Could not evaluate this conversation as a workflow")

    applicable = bool(payload["applicable"])
    try:
        draft = WorkflowDraft(
            name=payload.get("name") or "",
            description=payload.get("description") or "",
            instructions=payload.get("instructions") or "",
            input_question=payload.get("input_question") or "",
        )
    except Exception as exc:
        raise AgentError("Could not evaluate this conversation as a workflow") from exc
    return WorkflowSuggestion(applicable=applicable, draft=draft)


async def evaluate_workflow_suggestion(
    messages: list[ChatMessage],
    *,
    albert: DraftChatClient | None,
    model: str | None,
) -> WorkflowSuggestion:
    """Ask the model whether ``messages`` is workflow-worthy, and generalize it."""
    if albert is None or model is None:
        return _fallback_suggestion(messages)

    prompt_messages: list[dict[str, Any]] = [
        {"role": "system", "content": SUGGESTION_SYSTEM_PROMPT},
        *(
            message.model_dump(include={"role", "content"})
            for message in messages
        ),
    ]
    content_parts: list[str] = []
    async for chunk in albert.chat_completion_stream(
        model=model, messages=prompt_messages, tools=[]
    ):
        if chunk["type"] == "content":
            content_parts.append(chunk["delta"])

    raw = "".join(content_parts).strip()
    if not raw:
        raise AgentError("Could not evaluate this conversation as a workflow")
    return _parse_suggestion(raw)
