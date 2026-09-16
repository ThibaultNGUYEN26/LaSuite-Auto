"""Groups registered specialist agents into user-facing specializations.

The registry itself only knows about individual tools (``drive_list_items``,
``local_files_read_pdf``, ...); this groups them by the capability area an
end user would recognize and want to toggle, for the settings UI.
"""

from __future__ import annotations

from agent.orchestrator import build_agent_registry
from schemas import AgentSpecializationOut, SpecialistToolOut

# (id, display name, description, tool-name prefix). The last entry with a
# ``None`` prefix is the catch-all for tools that don't match another group.
_SPECIALIZATION_DEFS: list[tuple[str, str, str, str | None]] = [
    (
        "drive",
        "La Suite Drive",
        "Read, list, and create files in La Suite Drive.",
        "drive_",
    ),
    (
        "local_files",
        "Local files",
        "Read, list, and create files on the local filesystem.",
        "local_files_",
    ),
    (
        "code",
        "Code execution",
        "Run short Python snippets for calculations and data wrangling.",
        None,
    ),
]


def list_specializations() -> list[AgentSpecializationOut]:
    """Return every specialization the orchestrator can currently route to."""
    registry = build_agent_registry()

    tools_by_id: dict[str, list[SpecialistToolOut]] = {
        spec_id: [] for spec_id, *_ in _SPECIALIZATION_DEFS
    }
    catch_all_id = next(
        spec_id for spec_id, _, _, prefix in _SPECIALIZATION_DEFS if prefix is None
    )

    for definition in registry.tool_definitions():
        function = definition["function"]
        tool = SpecialistToolOut(name=function["name"], description=function["description"])
        for spec_id, _, _, prefix in _SPECIALIZATION_DEFS:
            if prefix is not None and tool.name.startswith(prefix):
                tools_by_id[spec_id].append(tool)
                break
        else:
            tools_by_id[catch_all_id].append(tool)

    return [
        AgentSpecializationOut(
            id=spec_id,
            name=name,
            description=description,
            enabled=True,
            tools=tools_by_id[spec_id],
        )
        for spec_id, name, description, _ in _SPECIALIZATION_DEFS
    ]
