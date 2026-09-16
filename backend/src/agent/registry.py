"""Registry used by the orchestrator to discover and call specialist agents."""

from __future__ import annotations

import json
import inspect
from collections.abc import Iterable
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import AgentError


class AgentRegistry:
    def __init__(self, agents: Iterable[SpecialistAgent] = ()) -> None:
        self._agents: dict[str, SpecialistAgent] = {}
        for agent in agents:
            self.register(agent)

    def register(self, agent: SpecialistAgent) -> None:
        if not agent.name:
            raise ValueError("A specialist agent must have a name")
        if agent.name in self._agents:
            raise ValueError(f"Specialist agent already registered: {agent.name}")
        self._agents[agent.name] = agent

    def tool_definitions(self) -> list[dict[str, Any]]:
        return [agent.tool_definition() for agent in self._agents.values()]

    def dispatch(
        self, name: str, raw_arguments: str, context: DelegationContext
    ) -> dict[str, Any]:
        agent = self._agents.get(name)
        if agent is None:
            return {"error": f"Unknown specialist agent: {name}"}

        try:
            arguments = json.loads(raw_arguments or "{}")
        except (json.JSONDecodeError, TypeError) as exc:
            message = exc.msg if isinstance(exc, json.JSONDecodeError) else str(exc)
            return {"error": f"Invalid agent arguments: {message}"}
        if not isinstance(arguments, dict):
            return {"error": "Agent arguments must be a JSON object"}

        try:
            result = agent.execute(arguments, context)
        except AgentError as exc:
            return {"error": str(exc)}
        if inspect.isawaitable(result):
            close = getattr(result, "close", None)
            if callable(close):
                close()
            return {
                "error": (
                    f"Specialist agent {name} is asynchronous; use async dispatch"
                )
            }
        if not isinstance(result, dict):
            return {"error": f"Specialist agent {name} returned an invalid result"}
        return result

    async def dispatch_async(
        self, name: str, raw_arguments: str, context: DelegationContext
    ) -> dict[str, Any]:
        """Dispatch either a synchronous or asynchronous specialist."""
        agent = self._agents.get(name)
        if agent is None:
            return {"error": f"Unknown specialist agent: {name}"}

        try:
            arguments = json.loads(raw_arguments or "{}")
        except (json.JSONDecodeError, TypeError) as exc:
            message = exc.msg if isinstance(exc, json.JSONDecodeError) else str(exc)
            return {"error": f"Invalid agent arguments: {message}"}
        if not isinstance(arguments, dict):
            return {"error": "Agent arguments must be a JSON object"}

        try:
            result = agent.execute(arguments, context)
            if inspect.isawaitable(result):
                result = await result
        except AgentError as exc:
            return {"error": str(exc)}
        if not isinstance(result, dict):
            return {"error": f"Specialist agent {name} returned an invalid result"}
        return result
