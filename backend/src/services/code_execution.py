"""Run untrusted Python snippets in a bounded subprocess."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from agent.errors import CodeExecutionError
from config import settings

MAX_TIMEOUT_SECONDS = 30


def _run_subprocess(
    command: list[str], *, timeout: int, cwd: str | Path | None = None
) -> dict[str, Any]:
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
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
            timeout=timeout,
            cwd=cwd,
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


def run_python_code(
    code: str, *, timeout: int = 10, cwd: str | Path | None = None
) -> dict[str, Any]:
    if not isinstance(code, str) or not code.strip():
        raise CodeExecutionError("code must be a non-empty string")

    return _run_subprocess([sys.executable, "-c", code], timeout=timeout, cwd=cwd)


def run_python_file(
    path: str | Path,
    args: list[str] | None = None,
    timeout: int = 10,
    cwd: str | Path | None = None,
) -> dict[str, Any]:
    if not isinstance(path, (str, Path)) or not str(path).strip():
        raise CodeExecutionError("path must be a non-empty path")

    resolved_root = settings.local_files_root.expanduser().resolve()
    candidate = (resolved_root / str(path)).resolve()
    try:
        candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise CodeExecutionError("path escapes the configured local-files root") from exc
    if not candidate.exists():
        raise CodeExecutionError("File does not exist")
    if not candidate.is_file():
        raise CodeExecutionError("Path is not a file")
    if candidate.suffix.lower() != ".py":
        raise CodeExecutionError("Path must be a .py file")
    if args is None:
        args = []
    if not isinstance(args, list) or not all(isinstance(argument, str) for argument in args):
        raise CodeExecutionError("args must be a list of strings")

    return _run_subprocess(
        [sys.executable, str(candidate), *args],
        timeout=timeout,
        cwd=cwd,
    )
