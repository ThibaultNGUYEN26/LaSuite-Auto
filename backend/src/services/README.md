# Services

The service layer contains reusable backend logic that is shared across agents, providers, and routes. These functions are lower-level than the orchestrator but higher-level than raw HTTP or DB interactions.

## Current responsibilities

### `chat_title.py`
Generates a concise title from the first user prompt and assistant response.

This is used when the frontend or backend needs a preview title for a new conversation.

### `drive.py`
Low-level authenticated access to La Suite Drive.

It handles:

- Drive config lookup
- Drive item listing
- item metadata retrieval
- ACL resolution
- file upload and folder traversal helpers
- authenticated headers and cookie handling

This module is the integration layer underneath the drive specialists.

### `local_files.py`
Utilities for resolving and validating local paths under `LOCAL_FILES_ROOT`.

It is used to ensure local filesystem operations remain scoped to the configured root and avoid path traversal issues.

### `pdf_memory.py`
Creates durable Markdown memories for PDFs.

Responsibilities include:

- splitting large PDFs into page-based chunks
- sending chunked synthesis requests to the model
- reducing notes and deduplicating content
- storing the final memory under the managed memory directory
- preserving citations and metadata around the source document

### `pdf_search.py`
Search and ranking utilities for relevant PDF sections and page content.

### `text_content.py`
Helpers for decoding BOM- and encoding-aware text content from files and downloaded Drive documents.

### `pdf_report.py`, `pdf_audit.py`, `pdf_comparison.py`, `tabular_analysis.py`
These modules implement higher-level document-analysis and reporting operations used by the specialist blocks. They are not human-facing APIs by themselves; they are reusable execution building blocks for the domain-specific agents.

### `code_execution.py`
A bounded code-execution helper used when specialist capabilities need to run script-based logic inside the backend environment.

## Design principles

- Services encapsulate reusable logic, not route handlers.
- They should be domain-focused and testable in isolation.
- Auth, path validation, and resource limits remain here so the specialist agents stay concise.
- They should not contain orchestrator policy or general model selection logic.

## Related docs

- [backend/src/agent/README.md](../agent/README.md)
- [backend/src/providers/README.md](../providers/README.md)
- [backend/src/repositories/README.md](../repositories/README.md)
- [backend/README.md](../../README.md)
