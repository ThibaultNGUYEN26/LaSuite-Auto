"""Contract implemented by every specialist agent."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections.abc import Awaitable
from typing import Any, Sequence

from schemas import ChatMessage


@dataclass(frozen=True)
class DelegationContext:
    """Request context passed to a specialist during one delegation."""

    conversation: Sequence[ChatMessage]


class SpecialistAgent(ABC):
    """A capability that the orchestrator can advertise and invoke."""

    name: str
    description: str
    parameters: dict[str, Any]

    def tool_definition(self) -> dict[str, Any]:
        """Return this agent in Albert's OpenAI-compatible tool format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    @abstractmethod
    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any] | Awaitable[dict[str, Any]]:
        """Execute one delegation and return JSON-serializable data."""
