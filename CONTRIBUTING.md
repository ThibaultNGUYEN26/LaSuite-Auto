# Contributing to Auto

Thanks for helping improve Auto.

This project is designed as a modular AI orchestration platform for La Suite workflows. Contributions should stay focused on improving the orchestration layer, capabilities, integrations, or developer experience without breaking the overall architecture.

## Project structure

- `app/` — Electron desktop application
- `backend/` — backend API, orchestration logic, providers, services, and specialist integrations
- `docs/` — project documentation and design notes
- `README.md` — project overview and product pitch

## Before contributing

1. Read the project overview in [README.md](README.md).
2. Read the backend documentation in [backend/README.md](backend/README.md).
3. Review the architecture docs in [backend/src/README.md](backend/src/README.md) and [backend/src/agent/README.md](backend/src/agent/README.md).
4. Keep changes aligned with the existing capability-block design.

## Development workflow

### 1. Create a branch

Use a descriptive branch name:

```bash
git checkout -b feat/my-change
```

### 2. Install dependencies

Follow the setup instructions in the relevant project README before running code.

### 3. Make focused changes

Keep pull requests small and targeted. Prefer one well-scoped change per PR.

### 4. Validate locally

Before opening a PR:

- run the relevant tests or checks for the area you changed
- ensure the backend still starts correctly
- confirm documentation reflects the code change

## Coding conventions

- Keep the orchestrator generic and integration-agnostic.
- Prefer structured artifacts and typed tool results over ad hoc model reasoning.
- Respect filesystem boundaries, authentication requirements, and permission scopes.
- Avoid hardcoding environment-specific values.
- Keep new capability blocks self-contained and discoverable.

## Block and integration guidelines

If you add a new capability or specialist:

- place it in the appropriate domain under `backend/src/agent/specialists/`
- expose a `create_block()` factory
- declare required config and permissions clearly
- validate model-provided arguments before external actions
- return structured results that downstream agents can reuse

## Documentation

When changing behavior, also update the relevant documentation in:

- [README.md](README.md)
- [backend/README.md](backend/README.md)
- the corresponding backend source READMEs under `backend/src/`
- API docs if the change affects exposed endpoints or tool contracts

## Pull requests

A good PR should include:

- a clear summary of the change
- the motivation and context
- any impacted docs or config
- validation steps or test commands used

## Questions

If you are unsure where a change belongs, start by checking the architecture docs and the relevant source folder. Small design questions are usually best answered by following the existing block and service boundaries.

Thank you for contributing to Auto.
