from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


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
