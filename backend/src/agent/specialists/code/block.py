"""Code-execution capability block."""

from agent.blocks import AgentBlock, CapabilityManifest
from agent.specialists.code import RunPythonAgent


def create_block() -> AgentBlock:
    return AgentBlock(
        name="code",
        description=(
            "Execute bounded custom Python tasks as a fallback when no dedicated "
            "block covers the request. Do not use it for tabular analysis when a "
            "data-analysis capability is available."
        ),
        agents=(RunPythonAgent(),),
        permissions=("process.execute",),
        capabilities=(
            CapabilityManifest(
                name="run_python",
                description=(
                    "Execute bounded Python code and return its output. This is a "
                    "fallback for custom computation, not the preferred capability "
                    "for CSV, spreadsheet, or trend analysis."
                ),
                side_effect="code_execution",
                permissions=("process.execute",),
                confirmation_required=True,
            ),
        ),
    )
