# Backend source

This directory contains the application logic for the orchestration backend. It is organized into a few core layers:

- `agent/` — reasoning loop, block discovery, and capability implementations
- `providers/` — model-provider adapters such as Albert and the echo fallback
- `repositories/` — SQLAlchemy persistence for chats and workflows
- `services/` — reusable backend logic for titles, PDF memory, file handling, and integrations
- `config.py`, `db.py`, `main.py`, `models.py`, `schemas.py` — runtime configuration, database setup, application bootstrap, and shared schemas

## High-level flow

```text
HTTP request
  -> FastAPI app
  -> orchestration layer
  -> selected capability block
  -> provider or external integration
  -> structured result/artifact
```

The orchestrator is intentionally generic: it does not know about Drive or local files directly. Instead, it discovers blocks and tools, then delegates to the relevant specialist agents.

## Key directories

### `agent/`
Contains the planning loop and the capability system. It is where the model interacts with available tools and where specialist blocks are wrapped into a runtime registry.

### `providers/`
Contains the adapters used to talk to external LLM backends, especially Albert. Providers are kept behind a small interface so the orchestrator does not depend on one vendor implementation.

### `repositories/`
Contains persistence logic for the database-backed chat and workflow records.

### `services/`
Contains reusable domain logic such as Drive access, local file safety, PDF memory generation, and document-search support. These are shared building blocks for the specialist agents.

## Project conventions

- Keep orchestration logic separate from domain integrations.
- Prefer structured artifacts over large raw payloads in the orchestrator.
- Scoping and validation are required for filesystem and external API operations.
- Each block should declare its permissions and configuration needs explicitly.

## Related docs

- [agent/README.md](agent/README.md)
- [agent/specialists/README.md](agent/specialists/README.md)
- [providers/README.md](providers/README.md)
- [repositories/README.md](repositories/README.md)
- [services/README.md](services/README.md)
- [../README.md](../README.md)
