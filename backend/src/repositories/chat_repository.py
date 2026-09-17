"""CRUD operations for the Chat entity."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Chat, ChatMessageRow
from schemas import ChatCreate, ChatMessage


def create(db: Session, draft: ChatCreate) -> Chat:
    chat = Chat(
        title=draft.title,
        messages=[
            ChatMessageRow(position=i, role=m.role, content=m.content, trace=m.trace)
            for i, m in enumerate(draft.messages)
        ],
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def save_history(
    db: Session, chat_id: str, messages: list[ChatMessage]
) -> Chat:
    chat = db.get(Chat, chat_id)
    title = next(
        (message.content for message in messages if message.role == "user"),
        "New conversation",
    )
    if chat is None:
        chat = Chat(id=chat_id, title=title[:200])
        db.add(chat)
    else:
        chat.messages.clear()

    chat.messages.extend(
        ChatMessageRow(
            position=i, role=message.role, content=message.content, trace=message.trace
        )
        for i, message in enumerate(messages)
    )
    db.commit()
    db.refresh(chat)
    return chat


def list_all(db: Session) -> list[Chat]:
    stmt = select(Chat).order_by(Chat.updated_at.desc())
    return list(db.scalars(stmt))


def get(db: Session, chat_id: str) -> Chat | None:
    return db.get(Chat, chat_id)


def delete(db: Session, chat_id: str) -> bool:
    chat = db.get(Chat, chat_id)
    if chat is None:
        return False
    db.delete(chat)
    db.commit()
    return True


def append_message(db: Session, chat_id: str, message: ChatMessage) -> Chat | None:
    chat = db.get(Chat, chat_id)
    if chat is None:
        return None
    chat.messages.append(
        ChatMessageRow(
            position=len(chat.messages),
            role=message.role,
            content=message.content,
            trace=message.trace,
        )
    )
    db.commit()
    db.refresh(chat)
    return chat


def rename(db: Session, chat_id: str, title: str) -> Chat | None:
    chat = db.get(Chat, chat_id)
    if chat is None:
        return None
    chat.title = title
    db.commit()
    db.refresh(chat)
    return chat
