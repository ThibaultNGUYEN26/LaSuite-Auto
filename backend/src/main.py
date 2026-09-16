from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from agent.errors import AgentError
from agent.events import AgentEvent
from agent.runtime import draft_workflow_from_messages, run_stream
from agent.specializations import list_specializations

from config import settings
from db import get_db, init_db
from repositories import chat_repository
from repositories import workflow_repository
from schemas import (
    AgentSpecializationOut,
    ChatMessage,
    ChatRead,
    ChatRequest,
    WorkflowCreate,
    WorkflowDraftRequest,
    WorkflowOut,
)

app = FastAPI(title="Auto backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


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
        try:
            async for event in run_stream(request.messages):
                if await http_request.is_disconnected():
                    return
                if chat_id and event.type == "final":
                    chat_repository.save_history(
                        db,
                        chat_id,
                        [
                            *request.messages,
                            ChatMessage(role="assistant", content=event.data["content"]),
                        ],
                    )
                yield event.to_sse()
        except AgentError as exc:
            yield AgentEvent(
                "error", {"message": str(exc), "error_type": type(exc).__name__}
            ).to_sse()

    return StreamingResponse(
        event_source(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


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
