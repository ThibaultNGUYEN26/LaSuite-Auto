from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from agent.errors import AgentError
from agent.events import AgentEvent
from agent.orchestrator import run_stream
from config import settings
from schemas import ChatRequest

app = FastAPI(title="Auto backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest, http_request: Request) -> StreamingResponse:
    """Stream orchestrator progress and answer tokens as Server-Sent Events.

    Once the response has started, a 200 status and its headers are already
    on the wire, so a failure mid-stream is reported as an ``error`` SSE
    event instead of an HTTP error status.
    """

    async def event_source():
        try:
            async for event in run_stream(request.messages):
                if await http_request.is_disconnected():
                    return
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
