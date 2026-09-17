import mimetypes

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from agent.errors import AgentError, LocalFilesError
from agent.events import AgentEvent
from agent.runtime import (
    close_runtime,
    draft_workflow_from_messages,
    generate_chat_title,
    run_stream,
)
from agent.specializations import list_specializations

from config import settings
from db import get_db, init_db
from repositories import chat_repository
from repositories import workflow_repository
from services.local_files import resolve_local_file
from schemas import (
    AgentSpecializationOut,
    ChatMessage,
    ChatRead,
    ChatRequest,
    ChatTitleRequest,
    ChatTitleResponse,
    WorkflowCreate,
    WorkflowDraftRequest,
    WorkflowOut,
)

app = FastAPI(title="Auto backend")

VIEWABLE_EVIDENCE_EXTENSIONS = {
    ".pdf", ".csv", ".tsv", ".txt", ".md", ".json", ".yaml", ".yml", ".log"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await close_runtime()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/local-files/view", response_class=FileResponse)
def view_local_evidence(
    path: str,
    page: int = Query(default=1, ge=1),
) -> FileResponse:
    """Open local audit evidence inline; PDF URL fragments select the page."""
    del page  # Browser PDF viewers consume the matching #page=N fragment.
    try:
        source = resolve_local_file(settings.local_files_root, path)
    except LocalFilesError as exc:
        raise HTTPException(status_code=404, detail="Evidence file not found") from exc
    if source.suffix.lower() not in VIEWABLE_EVIDENCE_EXTENSIONS:
        raise HTTPException(status_code=422, detail="This evidence type cannot be viewed")
    return FileResponse(
        source,
        media_type=mimetypes.guess_type(source.name)[0] or "application/octet-stream",
        filename=source.name,
        content_disposition_type="inline",
    )


@app.post("/api/conversations/new")
def new_conversation() -> dict[str, str]:
    """Acknowledge a new-conversation request.

    The renderer creates the conversation ID when the chat view mounts and
    persists its history with the first stream request.
    """
    return {"status": "ok"}


@app.get("/api/conversations")
def list_conversations(db: Session = Depends(get_db)) -> list[ChatRead]:
    return [ChatRead.model_validate(chat) for chat in chat_repository.list_all(db)]


@app.delete("/api/conversations/{chat_id}")
def delete_conversation(chat_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    if not chat_repository.delete(db, chat_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "ok"}


@app.post("/api/chat/stream")
async def chat_stream(
    request: ChatRequest,
    http_request: Request,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    """Stream orchestrator progress and answer tokens as Server-Sent Events.

    Once the response has started, a 200 status and its headers are already
    on the wire, so a failure mid-stream is reported as an ``error`` SSE
    event instead of an HTTP error status.
    """

    chat_id = request.chat_id
    if chat_id:
        chat_repository.save_history(db, chat_id, request.messages)

    async def event_source():
        partial_content = ""
        # Mirrors the frontend's `applyStreamEvent` trace-building so a reopened
        # conversation's "View trace" panel matches what was shown live.
        trace: list[dict] = []
        tool_call_positions: dict[str, int] = {}

        def save_partial() -> None:
            if chat_id and (partial_content or trace):
                chat_repository.save_history(
                    db,
                    chat_id,
                    [
                        *request.messages,
                        ChatMessage(
                            role="assistant",
                            content=partial_content,
                            trace=trace or None,
                        ),
                    ],
                )

        try:
            async for event in run_stream(request.messages):
                if await http_request.is_disconnected():
                    save_partial()
                    return
                if event.type == "token":
                    partial_content += event.data["delta"]
                elif event.type == "step_start":
                    trace.append({"type": "step", "step": event.data["step"]})
                elif event.type == "tool_call_start":
                    tool_call_positions[event.data["tool_call_id"]] = len(trace)
                    trace.append(
                        {
                            "type": "tool_call",
                            "toolCallId": event.data["tool_call_id"],
                            "step": event.data["step"],
                            "name": event.data["name"],
                            "arguments": event.data["arguments"],
                        }
                    )
                elif event.type == "tool_call_result":
                    position = tool_call_positions.get(event.data["tool_call_id"])
                    if position is not None:
                        trace[position]["result"] = event.data["result"]
                if chat_id and event.type == "final":
                    chat_repository.save_history(
                        db,
                        chat_id,
                        [
                            *request.messages,
                            ChatMessage(
                                role="assistant",
                                content=event.data["content"],
                                trace=trace or None,
                            ),
                        ],
                    )
                yield event.to_sse()
        except AgentError as exc:
            save_partial()
            yield AgentEvent(
                "error", {"message": str(exc), "error_type": type(exc).__name__}
            ).to_sse()

    return StreamingResponse(
        event_source(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/api/conversations/title", response_model=ChatTitleResponse)
async def create_conversation_title(
    request: ChatTitleRequest,
    db: Session = Depends(get_db),
) -> ChatTitleResponse:
    """Generate a short display title from the conversation's first exchange."""
    try:
        title = await generate_chat_title(request.prompt, request.response)
    except AgentError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    if request.chat_id and chat_repository.rename(db, request.chat_id, title) is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ChatTitleResponse(title=title)


@app.get("/api/agent/specializations")
def get_agent_specializations() -> list[AgentSpecializationOut]:
    """List the specialist capability groups the orchestrator can route to.

    ``enabled`` is always ``True`` for now — there is no persistence layer
    for per-user preferences yet, so disabling a specialization here has no
    effect on the orchestrator. The UI setting exists as a preview of that
    future capability.
    """
    return list_specializations()


@app.post("/api/workflows/draft")
async def draft_workflow_route(request: WorkflowDraftRequest) -> dict[str, str]:
    try:
        draft = await draft_workflow_from_messages(request.messages)
    except AgentError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return draft.model_dump()


@app.get("/api/workflows")
def list_workflows(db: Session = Depends(get_db)) -> list[WorkflowOut]:
    return [
        WorkflowOut.model_validate(workflow)
        for workflow in workflow_repository.list_all(db)
    ]


@app.post("/api/workflows")
def create_workflow(
    body: WorkflowCreate, db: Session = Depends(get_db)
) -> WorkflowOut:
    workflow = workflow_repository.create(db, body)
    return WorkflowOut.model_validate(workflow)


@app.delete("/api/workflows/{workflow_id}")
def delete_workflow(workflow_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    if not workflow_repository.delete(db, workflow_id):
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"status": "ok"}
