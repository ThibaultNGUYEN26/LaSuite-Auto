# Repositories

The repository layer provides persistence access for the backend's SQLAlchemy models. It keeps DB read/write operations separate from request handling and agent orchestration.

## Current repositories

### `chat_repository.py`
Handles the persisted chat history and message rows.

Responsibilities:

- creating a new chat
- saving and replacing history for a given chat
- listing all chats
- fetching one chat by ID
- deleting a chat
- appending a message
- updating a chat title

This is the persistence layer used for conversation storage.

### `workflow_repository.py`
Handles saved workflow drafts and workflows.

Responsibilities:

- creating a workflow
- listing workflows in descending creation order
- fetching a workflow by ID
- deleting a workflow

## Data model layer

The repository layer relies on the ORM models defined in `backend/src/models.py`.

The main persisted entities are:

- `Workflow`
- `Chat`
- `ChatMessageRow`

These models are mapped to the application database and used by the FastAPI endpoints and orchestration backend.

## Interaction pattern

The repository functions accept a SQLAlchemy `Session` and encapsulate the actual SQLAlchemy operations. This keeps the rest of the backend code free of low-level persistence logic.

## Related docs

- [backend/src/agent/README.md](../agent/README.md)
- [backend/src/models.py](../models.py)
- [backend/README.md](../../README.md)
