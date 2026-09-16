from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    chat_id: str | None = None
    messages: list[ChatMessage]


class ChatTitleRequest(BaseModel):
    chat_id: str | None = None
    prompt: str = Field(min_length=1, max_length=8_000)
    response: str = Field(min_length=1, max_length=16_000)


class ChatTitleResponse(BaseModel):
    title: str


class WorkflowDraft(BaseModel):
    name: str
    description: str
    instructions: str
    input_question: str


class WorkflowDraftRequest(BaseModel):
    messages: list[ChatMessage]


class WorkflowCreate(BaseModel):
    name: str
    description: str
    instructions: str
    input_question: str


class WorkflowOut(BaseModel):
    id: str
    name: str
    description: str
    instructions: str
    input_question: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SpecialistToolOut(BaseModel):
    name: str
    description: str


class AgentSpecializationOut(BaseModel):
    id: str
    name: str
    description: str
    enabled: bool
    tools: list[SpecialistToolOut]


class ChatCreate(BaseModel):
    title: str
    messages: list[ChatMessage] = []


class ChatRead(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[ChatMessage]

    model_config = ConfigDict(from_attributes=True)
