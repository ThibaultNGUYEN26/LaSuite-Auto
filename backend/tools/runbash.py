import subprocess
from pydantic import BaseModel

class ToolCall(BaseModel):
    tool: Literal["readFile", "runbash", "runpython"]
    args: dict[str, Any]

class ToolResult(BaseModel):
    tool: str
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None


class RunBashArgs(BaseModel):
    command: str          # command string for now ? 
    timeout: int = 10

class RunBashResult(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool = False

def run_bash(args: RunBashArgs) -> RunBashResult:
    try:
        result = subprocess.run(
            args.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=args.timeout
        )
        return RunBashResult(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            timed_out=False
        )
    except subprocess.TimeoutExpired as e:
        return RunBashResult(
            stdout=e.stdout or "",
            stderr=e.stderr or "",
            exit_code=-1,
            timed_out=True
        )
    except Exception as e:
        return RunBashResult(
            stdout="",
            stderr=str(e),
            exit_code=-1,
            timed_out=False
        )