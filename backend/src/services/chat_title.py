"""Generate a concise display title from a chat's first exchange."""

from __future__ import annotations

import re
from typing import Any, Protocol

from agent.errors import AgentError

MAX_TITLE_LENGTH = 60

TITLE_SYSTEM_PROMPT = (
    "Create a concise title for a chat from its first user prompt and assistant "
    "response. Use the same language as the user. Capture the main intent, not "
    "implementation details. Use 3 to 8 words and at most 60 characters. Return "
    "only the title, with no quotes, label, markdown, or ending punctuation."
)


class TitleChatClient(Protocol):
    def chat_completion_stream(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ): ...


def _shorten(value: str, limit: int = MAX_TITLE_LENGTH) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) <= limit:
        return value
    shortened = value[: limit + 1].rsplit(" ", 1)[0].strip()
    return shortened or value[:limit].strip()


def normalize_title(raw: str, *, fallback_prompt: str) -> str:
    """Turn model output into a safe, single-line chat title."""
    title = next((line.strip() for line in raw.splitlines() if line.strip()), "")
    title = re.sub(r"^(?:title|titre)\s*:\s*", "", title, flags=re.IGNORECASE)
    title = title.strip(" \t\r\n`#*\"'“”«»")
    title = title.rstrip(".!?;:").strip()

    if not title:
        title = next(
            (line.strip() for line in fallback_prompt.splitlines() if line.strip()),
            "New conversation",
        )
    return _shorten(title)


def fallback_title(prompt: str) -> str:
    """Provide a useful title when no text-generation provider is configured."""
    return normalize_title("", fallback_prompt=prompt)


async def generate_title(
    prompt: str,
    response: str,
    *,
    albert: TitleChatClient,
    model: str,
) -> str:
    content_parts: list[str] = []
    async for chunk in albert.chat_completion_stream(
        model=model,
        messages=[
            {"role": "system", "content": TITLE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "First user prompt:\n"
                    f"{prompt}\n\n"
                    "First assistant response:\n"
                    f"{response}"
                ),
            },
        ],
        tools=[],
    ):
        if chunk.get("type") == "content" and isinstance(chunk.get("delta"), str):
            content_parts.append(chunk["delta"])

    raw = "".join(content_parts).strip()
    if not raw:
        raise AgentError("The title generator returned an empty response")
    return normalize_title(raw, fallback_prompt=prompt)
