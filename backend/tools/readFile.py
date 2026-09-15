class ToolCall(BaseModel):
    tool: Literal["readFile", "runbash", "runpython"]
    args: dict[str, Any]

class ToolResult(BaseModel):
    tool: str
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None

class ReadFileArgs(BaseModel):
    path: str

class ReadFileResult(BaseModel):
    content: Optional[str] = None
    error: Optional[str] = None

def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    text_parts = []
    for page in reader.pages:
        text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)

def read_file(args: ReadFileArgs) -> ReadFileResult:
    path = Path(args.path).resolve()
    try:
        if not path.exists():
            return ReadFileResult(error="File does not exist")
        if not path.is_file():
            return ReadFileResult(error="Path is not a file")
        if path.suffix.lower() != ".pdf":
            return ReadFileResult(error="Unsupported file type. Only PDF files are supported.")
        content = read_pdf(str(path))
        if not content.strip():
            return ReadFileResult(error="No extractable text (possibly a scanned/image PDF)")
        return ReadFileResult(content=content)
    except PermissionError:
        return ReadFileResult(error="Permission denied")
    except FileNotFoundError:
        return ReadFileResult(error="File not found")
    except Exception as e:
        return ReadFileResult(error=str(e))