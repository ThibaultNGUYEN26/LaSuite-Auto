# Backend README

This is the backend for the La Suite Automations project. It exposes the orchestration API, manages persistence, coordinates specialist capabilities, and integrates with external services such as Albert, La Suite Drive, Grist, and local file storage.

## What is in this backend?

The backend is organized into a few main layers:

- `src/agent/` — reasoning loop and capability-block system
- `src/providers/` — model provider adapters
- `src/repositories/` — database access for chats and workflows
- `src/services/` — reusable backend logic and integrations
- `src/config.py` and `src/main.py` — configuration and app entry points
- `src/models.py`, `src/schemas.py`, `src/db.py` — data layer and request schema definitions

For a more detailed map, see [src/README.md](src/README.md).

## Setup

Create a Python environment and install the backend dependencies:

```bash
uv sync
cp .env.example .env
uv run main.py
```

If the project already has a working environment, you can also run the backend directly from the backend directory using the configured command for your local shell.

## Configuration

Copy `.env.example` to `.env` and adjust the values you need. The most important settings include:

- `BACKEND_URL` — public URL used by the server, e.g. `http://127.0.0.1:8000`
- `AUTO_CORS_ORIGINS` — allowed origins for browser access
- `ALBERT_API_KEY` — API key for the default LLM provider
- `ALBERT_MODEL` — optional override for the text-generation model
- `ALBERT_VISION_MODEL` — optional vision model for image analysis
- `DRIVE_SESSION_ID` and `DRIVE_CSRF_TOKEN` — required for authenticated Drive actions
- `LOCAL_FILES_ROOT` — root directory for local file operations
- `GRIST_API_KEY`, `GRIST_ORG_ID`, `GRIST_WORKSPACE_ID` — Grist integration settings
- PDF and auditing limits such as `PDF_SEARCH_MAX_PAGES`, `PDF_MEMORY_MAX_BATCH_FILES`, and similar values

The backend reads these settings from environment variables and from the local `.env` file.

## Architecture at a glance

The runtime follows a capability-block design.

- `src/agent/orchestrator.py` contains the coordination loop.
- `src/agent/blocks.py` discovers built-in and installed blocks.
- `src/agent/registry.py` compiles specialist agents into a tool registry.
- `src/agent/selection.py` chooses relevant capabilities for a task.
- The specialist packages in `src/agent/specialists/` implement the domain logic for Drive, local files, PDFs, Grist, and analysis.

This means the orchestrator remains generic and does not need to know about each integration directly.

## Current capability domains

The current backend exposes a set of specialist domains:

- Drive: file browsing, reads, uploads, downloads, and folder operations
- Local files: bounded filesystem actions under `LOCAL_FILES_ROOT`
- PDF processing: creation, rendering, analysis, memory generation, and audit workflows
- Grist: CSV import and workspace discovery
- Data analysis: tabular analysis and PDF report rendering
- Code execution: script-based execution for bounded automation tasks

The exact list is defined in the block factory modules under `src/agent/specialists/`.

## Running the backend

From the `backend` directory:

```bash
uv run main.py
```

The app exposes the FastAPI server and the API endpoints documented in [API/backend-api.md](API/backend-api.md) and [API/README.md](API/README.md).

## API and documentation map

- [API/README.md](API/README.md) — unified documentation for the backend API and Drive client
- [API/backend-api.md](API/backend-api.md) — older redirect page to the merged backend API docs
- [src/README.md](src/README.md) — topology of the backend source tree
- [src/agent/README.md](src/agent/README.md) — runtime architecture and capability-block model
- [src/agent/specialists/README.md](src/agent/specialists/README.md) — block domains and specialist responsibilities
- [src/providers/README.md](src/providers/README.md) — model provider interface and active implementations
- [src/repositories/README.md](src/repositories/README.md) — persistence layer for chats and workflows
- [src/services/README.md](src/services/README.md) — reusable service logic for integrations and document workflows

## Typical workflow

A request usually follows this pattern:

1. The frontend sends a chat payload to the backend API.
2. The orchestrator loads the currently available blocks.
3. The model selects relevant specialist tools.
4. Those tools call external services or local file operations.
5. Structured artifacts are returned and reused during the same orchestration run.

This is the foundation for the PDF memory, audit, comparison, and data-analysis flows in the backend.

## Related files

- [src/main.py](src/main.py)
- [src/config.py](src/config.py)
- [src/agent/blocks.py](src/agent/blocks.py)
- [src/agent/orchestrator.py](src/agent/orchestrator.py)
- [src/agent/runtime.py](src/agent/runtime.py)
- [src/models.py](src/models.py)
- [src/schemas.py](src/schemas.py)
