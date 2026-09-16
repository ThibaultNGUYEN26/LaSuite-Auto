"""CRUD operations for the Workflow entity."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Workflow
from schemas import WorkflowCreate


def create(db: Session, draft: WorkflowCreate) -> Workflow:
    workflow = Workflow(
        name=draft.name,
        description=draft.description,
        instructions=draft.instructions,
        input_question=draft.input_question,
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow


def list_all(db: Session) -> list[Workflow]:
    stmt = select(Workflow).order_by(Workflow.created_at.desc())
    return list(db.scalars(stmt))


def get(db: Session, workflow_id: str) -> Workflow | None:
    return db.get(Workflow, workflow_id)


def delete(db: Session, workflow_id: str) -> bool:
    workflow = db.get(Workflow, workflow_id)
    if workflow is None:
        return False
    db.delete(workflow)
    db.commit()
    return True
