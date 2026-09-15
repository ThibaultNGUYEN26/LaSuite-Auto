"""Execute a short Python snippet in an isolated subprocess."""

from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import CodeExecutionError
from services.code_execution import MAX_TIMEOUT_SECONDS, run_python_code


class RunPythonAgent(SpecialistAgent):
    name = "run_python"
    description = (
        "Run a short Python code snippet in an isolated subprocess and return its "
        "stdout, stderr, and exit code. Use this for calculations, data processing, "
        "or checking what a piece of Python code does. The snippet has no access to "
        "the conversation, La Suite Drive, or local files unless it opens them itself."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python source code to execute.",
            },
            "timeout": {
                "type": "integer",
                "description": f"Maximum seconds to let the code run (1-{MAX_TIMEOUT_SECONDS}).",
                "default": 10,
            },
        },
        "required": ["code"],
        "additionalProperties": False,
    }

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        code = arguments.get("code")
        if not isinstance(code, str):
            raise CodeExecutionError("code must be a string")
        timeout = arguments.get("timeout", 10)
        if not isinstance(timeout, int):
            raise CodeExecutionError("timeout must be an integer")
        result = run_python_code(code, timeout=timeout)
        return {"status": "executed", **result}
