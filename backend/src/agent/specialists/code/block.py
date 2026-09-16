"""Code-execution capability block."""

from agent.blocks import AgentBlock, CapabilityManifest
from agent.specialists.code import RunPythonAgent


def create_block() -> AgentBlock:
    return AgentBlock(
        name="code",
        description="Execute bounded Python tasks.",
        agents=(RunPythonAgent(),),
        permissions=("process.execute",),
        capabilities=(
            CapabilityManifest(
                name="run_python",
                description="Execute bounded Python code and return its output.",
                side_effect="code_execution",
                permissions=("process.execute",),
                confirmation_required=True,
            ),
        ),
    )
