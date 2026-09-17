"""SQLite persistence for workflows: engine, session factory, table setup."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings


class Base(DeclarativeBase):
    pass


_db_path = Path(settings.db_path).expanduser()
_db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    f"sqlite:///{_db_path}", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    import models  # noqa: F401  (registers models on Base before create_all)

    Base.metadata.create_all(bind=engine)
    _ensure_chat_messages_trace_column()


def _ensure_chat_messages_trace_column() -> None:
    # `create_all` only creates missing tables, not missing columns on tables
    # that already exist on disk from before `trace` was added - there's no
    # migration tool in this project, so patch it in directly.
    with engine.connect() as conn:
        columns = {
            row[1] for row in conn.exec_driver_sql("PRAGMA table_info(chat_messages)")
        }
        if columns and "trace" not in columns:
            conn.exec_driver_sql("ALTER TABLE chat_messages ADD COLUMN trace JSON")
            conn.commit()


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
