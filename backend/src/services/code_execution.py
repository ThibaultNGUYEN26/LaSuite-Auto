"""Run untrusted Python snippets in a bounded subprocess."""

from __future__ import annotations

import os
import subprocess
import sys
from typing import Any

from agent.errors import CodeExecutionError

MAX_TIMEOUT_SECONDS = 30


def run_python_code(code: str, *, timeout: int = 10) -> dict[str, Any]:
    if not isinstance(code, str) or not code.strip():
        raise CodeExecutionError("code must be a non-empty string")
    if timeout <= 0 or timeout > MAX_TIMEOUT_SECONDS:
        raise CodeExecutionError(f"timeout must be between 1 and {MAX_TIMEOUT_SECONDS} seconds")

    environment = os.environ.copy()
    # Windows otherwise inherits a legacy console code page such as cp1252. The
    # snippets commonly process UTF-8 CSV data, so keep both the child streams
    # and the parent-side decoding explicitly UTF-8.
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
            timeout=timeout,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "exit_code": -1,
            "timed_out": True,
        }
