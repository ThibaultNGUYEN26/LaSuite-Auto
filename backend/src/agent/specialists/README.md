# Specialist blocks

This directory contains the capability-oriented integrations exposed to the orchestrator. Each subfolder is a domain block, and each block packages a set of model-facing agents behind a single discovery entry point.

## Structure

```text
backend/src/agent/specialists/
├── code/
├── data_analysis/
├── drive/
├── grist/
├── local_files/
├── pdf/
├── __init__.py
└── README.md
```

Each block is built around a `create_block()` function returning an `AgentBlock` object. The block defines:

- the block name and description
- required environment/config values
- declared permissions
- agent definitions
- workflow templates and capability manifests

## How specialists are used

The orchestrator does not directly call these modules. Instead, it receives the block manifests and then invokes the matching agent based on schema and capability descriptions.

This gives a clean separation between:

- the reasoning loop
- the model tool registry
- the integration logic for each domain

## Current domains

### `drive/`
Responsible for Drive discovery, file metadata, content reads, uploads, renames, and folder downloads. It is designed around Drive item references and authenticated session cookies.

Typical examples:

- `drive_list_items`
- `drive_read_pdf`
- `drive_search_pdfs`
- `drive_create_file`
- `drive_upload_file`
- `drive_download_folder`

### `local_files/`
Responsible for safe filesystem interaction underneath `LOCAL_FILES_ROOT`. It supports reading PDFs, indexing memory caches, creating files/folders, folder analysis, comparison, and audits.

Typical examples:

- `local_files_list_items`
- `local_files_create_file`
- `local_files_create_folder`
- `local_files_read_pdf`
- `local_files_summarize_pdf`
- `local_files_audit_folder`
- `local_files_compare_pdfs`

### `pdf/`
Responsible for PDF generation and editing workflows. This includes creating simple PDFs, rendering analysis reports, applying Typst templates, and running bounded script-based PDF transformations.

Typical examples:

- `pdf_create`
- `pdf_render_analysis`
- `pdf_apply_template`
- `pdf_run_script`

### `grist/`
Responsible for Grist-specific import flows and workspace discovery. It accepts CSV content or local file references and imports them into a workspace.

Typical examples:

- `grist_list_workspaces`
- `grist_import_csv`

### `data_analysis/`
Responsible for structured table analysis. It consumes CSV/ODS/Grist datasets and produces a data-analysis artifact that can be rendered into a PDF report.

Typical examples:

- `data_analyze_table`
- `pdf_render_analysis`

### `code/`
Responsible for code-oriented execution and tool integrations that are not purely document or file operations.

## Contributor rules

When adding a new capability, keep these principles in mind:

- Keep the block self-contained.
- Validate all model-supplied arguments before performing external actions.
- Return structured results rather than a pre-written assistant response.
- Respect explicit path boundaries, permissions, and max-byte limits.
- Prefer typed artifacts and references over large raw payloads in the orchestrator.

## Example block pattern

Each specialist package typically contains:

- `block.py` — exported `create_block()` factory
- agent implementation modules
- helper functions and validation logic
- any internal utility code needed for the domain

The block is the public boundary; the orchestrator never depends on a package by name beyond the discovered block registry.

## Related docs

- [backend/src/agent/README.md](../README.md)
- [backend/BLOCKS.md](../../BLOCKS.md)
