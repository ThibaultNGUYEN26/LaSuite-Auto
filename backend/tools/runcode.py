import subprocess
import sys
from pydantic import BaseModel

class RunPythonArgs(BaseModel):
    code: str
    timeout: int = 10

class RunPythonResult(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool = False

def run_python(args: RunPythonArgs) -> RunPythonResult:
    try:
        result = subprocess.run(
            [sys.executable, "-c", args.code],
            capture_output=True,
            text=True,
            timeout=args.timeout
        )
        return RunPythonResult(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            timed_out=False
        )
    except subprocess.TimeoutExpired as e:
        return RunPythonResult(
            stdout=e.stdout or "",
            stderr=e.stderr or "",
            exit_code=-1,
            timed_out=True
        )