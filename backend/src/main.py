from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent.orchestrator import run
from config import settings
from schemas import ChatRequest, ChatResponse

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


@app.post("/api/chat")
def chat(request: ChatRequest) -> ChatResponse:
    reply = run(request.messages)
    return ChatResponse(reply=reply)
