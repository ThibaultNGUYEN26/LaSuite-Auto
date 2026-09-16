"""Groups registered capability blocks into user-facing specializations.

Each ``AgentBlock`` already carries the display name, description, and
capability manifests an end user would recognize and want to toggle, so this
module simply adapts that block metadata for the settings UI.
"""

from __future__ import annotations

from agent.blocks import BlockRegistry
from schemas import AgentSpecializationOut, SpecialistToolOut


def list_specializations() -> list[AgentSpecializationOut]:
    """Return every specialization the orchestrator can currently route to."""
    registry = BlockRegistry.discover()

    return [
        AgentSpecializationOut(
            id=block["name"],
            name=block["name"],
            description=block["description"],
            enabled=True,
            tools=[
                SpecialistToolOut(name=capability["name"], description=capability["description"])
                for capability in block["capabilities"]
            ],
        )
        for block in registry.catalog()
    ]
