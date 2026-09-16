"""Execute a short Python snippet in an isolated subprocess."""

from pathlib import Path
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import CodeExecutionError
from services.code_execution import MAX_TIMEOUT_SECONDS, run_python_code, run_python_file
from services.local_files import resolve_local_file


class RunPythonAgent(SpecialistAgent):
    name = "run_python"
    description = (
        "Run a short Python code snippet in an isolated subprocess and return its "
        "stdout, stderr, and exit code. Use this for calculations, data processing, "
        "or checking what a piece of Python code does. The snippet has no access to "
        "the conversation, La Suite Drive, or local files unless it opens them itself. "
        "For PDF creation, templating, or scripted PDF edits, use the pdf block's "
        "tools instead."
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


class RunPythonFileAgent(SpecialistAgent):
    name = "run_python_file"
    description = (
        "Run a Python file in an isolated subprocess. The file must be inside the "
        "configured local-files root. Return its stdout, stderr, and exit code. For "
        "PDF creation, templating, or scripted PDF edits, use the pdf block's tools "
        "instead."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": (
                    "Path to a Python file relative to the configured local-files root."
                ),
            },
            "args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional command-line arguments for the Python file.",
                "default": [],
            },
            "timeout": {
                "type": "integer",
                "description": f"Maximum seconds to let the file run (1-{MAX_TIMEOUT_SECONDS}).",
                "default": 10,
            },
        },
        "required": ["path"],
        "additionalProperties": False,
    }

    def __init__(self, root: Path) -> None:
        self.root = root

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        path = arguments.get("path")
        if not isinstance(path, str):
            raise CodeExecutionError("path must be a string")
        args = arguments.get("args", [])
        if not isinstance(args, list) or not all(isinstance(argument, str) for argument in args):
            raise CodeExecutionError("args must be a list of strings")
        timeout = arguments.get("timeout", 10)
        if not isinstance(timeout, int):
            raise CodeExecutionError("timeout must be an integer")

        resolved_path = resolve_local_file(self.root, path)
        result = run_python_file(resolved_path, args=args, timeout=timeout)
        return {"status": "executed", **result}
