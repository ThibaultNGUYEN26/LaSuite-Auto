# Specialist agent integration

The orchestrator is a coordinator. It does not implement filesystem or Python
execution itself. Instead, it advertises registered specialist agents to the
model as tools and dispatches the selected call through `AgentRegistry`.

## Routing flow

1. `OrchestratorAgent` sends the conversation and registered tool definitions
   to Albert.
2. Albert selects the specialist whose description and parameter schema match
   the user's intent.
3. `AgentRegistry` parses the arguments and invokes that specialist.
4. The structured result is returned to Albert, which may delegate another step
   or produce the final response.

## Adding the Python execution agent

Implement `SpecialistAgent` in a separate module:

```python
from typing import Any

from agent.base import DelegationContext, SpecialistAgent


class PythonExecutionAgent(SpecialistAgent):
    name = "python_execute"
    description = (
        "Execute an approved Python-based operation on local files, such as "
        "classifying or organizing files in the user's Downloads folder."
    )
    parameters = {
        "type": "object",
        "properties": {
            "task": {"type": "string"},
            "working_directory": {"type": "string"},
        },
        "required": ["task", "working_directory"],
        "additionalProperties": False,
    }

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        # Delegate to the sandboxed Python runner here.
        return {
            "status": "completed",
            "summary": "...",
            "files_changed": [],
        }
```

Register it in `build_agent_registry()` in `orchestrator.py`. Once registered,
its definition is automatically sent to Albert; no routing `if` statement is
needed in the orchestration loop.

The Python agent should resolve and enforce an allowed workspace itself. It
must not trust a model-provided path, and destructive operations should require
an explicit approval flow. Return structured results and errors rather than a
prewritten assistant response so the coordinator can combine several agents.
