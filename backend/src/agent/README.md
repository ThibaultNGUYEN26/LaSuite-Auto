# Agent architecture

The backend is structured around a reusable planning loop and a set of domain-specific capability blocks. The orchestrator does not know about Drive, local files, PDFs, or Grist directly; it only sees the capabilities that are discovered at startup.

The current runtime flow is:

1. `agent.blocks` discovers built-in and installed blocks.
2. Each block exposes one or more `SpecialistAgent` objects.
3. `AgentRegistry` compiles those agents into a single callable registry.
4. `OrchestratorAgent` asks the model to select the most relevant capabilities, then executes them in order.
5. Results are returned as typed artifacts and reused by later steps.

This keeps the reasoning engine generic while letting integrations evolve without editing the orchestrator itself.

## Folder layout

```text
backend/src/
├── agent/
│   ├── base.py
│   ├── blocks.py
│   ├── errors.py
│   ├── events.py
│   ├── orchestrator.py
│   ├── registry.py
│   ├── runtime.py
│   ├── selection.py
│   ├── README.md
│   ├── specialists/
│   │   ├── code/
│   │   ├── data_analysis/
│   │   ├── drive/
│   │   ├── grist/
│   │   ├── local_files/
│   │   ├── pdf/
│   │   └── README.md
│   ├── workflow_synthesizer.py
│   └── ...
├── providers/
│   ├── albert.py
│   ├── base.py
│   ├── echo.py
│   └── README.md
├── repositories/
│   ├── chat_repository.py
│   ├── workflow_repository.py
│   └── README.md
├── services/
│   ├── chat_title.py
│   ├── drive.py
│   ├── local_files.py
│   ├── pdf_memory.py
│   ├── pdf_search.py
│   ├── text_content.py
│   ├── ...
│   └── README.md
├── config.py
├── db.py
├── main.py
├── models.py
├── schemas.py
└── ...
```

## Runtime and block composition

The runtime entry point is in [backend/src/runtime.py](../runtime.py) via the app composition layer, but the operational logic is split as follows:

- `agent.blocks` defines discovery, manifest metadata, and block validation.
- `agent.registry` wraps the selected specialist agents in a tool registry.
- `agent.selection` picks the relevant block(s) and capabilities for a request.
- `agent.orchestrator` runs the multi-step reasoning loop with the selected tools.
- `agent.workflow_synthesizer` turns a conversation into a reusable workflow draft.

The block manifest system is the contract between the orchestrator and the integrations:

- Each block has a name, description, permissions, and optional workflow definitions.
- Each capability has a name, side effect classification, accepted artifact kinds, produced artifact kinds, and explicit config requirements.
- Capabilities can be tagged as `internal` when they are preparation steps rather than user-visible actions.

The orchestrator sees only these manifests at the first stage; it does not directly import the concrete integration code.

## Built-in capability domains

### Drive
The Drive block is responsible for reading, creating, renaming, and downloading content in La Suite Drive. It includes capabilities such as:

- `drive_list_items`
- `drive_get_config`
- `drive_read_pdf`
- `drive_search_pdfs`
- `drive_read_text`
- `drive_create_file`
- `drive_create_files`
- `drive_upload_file`
- `drive_download_folder`
- `drive_rename_file`
- `drive_read_image`

These calls are wrapped with authenticated session handling and bounded traversal/download limits.

### Local files
The local-files block manages the configured `LOCAL_FILES_ROOT` and provides safe filesystem operations. It covers:

- listing and creating local folders/files
- bounded PDF text extraction
- memory creation for durable PDF summaries
- folder-level analysis and audit workflows
- comparing two PDFs and auditing against a reference PDF
- image and text reading

The most important pattern is that PDF memory generation is treated as an internal preparation step: the user asks for understanding, review, or analysis, and the system prepares the memory automatically when needed.

### PDF processing
The PDF specialists handle direct document creation, tailored rendering, and script-driven PDF edits. They are designed to keep PDF-specific work in the PDF block instead of leaking library concerns into the orchestrator.

### Grist
The Grist block integrates CSV import and workspace discovery, enabling backend agents to send structured tabular data into Grist without exposing all of the REST detail to the orchestrator.

### Data analysis
The data-analysis block accepts CSV/ODS/Grist artifacts and produces a structured analysis result that can later be rendered into a PDF report.

### Code execution
The code execution block is a lower-level specialist family used for script-based tasks and bounded runtime actions. It is intentionally narrow and should be treated as a specialized capability rather than as a general-purpose unrestricted executor.

## Routing flow

1. The user sends a conversation to the backend.
2. The orchestrator loads the registered capability blocks.
3. The model receives compact block manifests and chooses the relevant tools.
4. Tool arguments are validated by the selected agent.
5. Execution returns structured results and artifacts.
6. The model may decide to call more tools or provide the final answer.

The key design principle is that structured artifacts are reused across steps. Example: a file reference returned by `drive_list_items` is fed into `drive_read_pdf`, and a report artifact produced by analysis can be rendered into a PDF later without reconstructing the original data in the LLM.

## Safety and permissions

Each block declares permissions and config requirements. These are not cosmetic: they define what the model is allowed to do and what environment values must be present before the block can be used.

Examples include:

- `local.read` / `local.write`
- `drive.read` / `drive.write`
- `model.vision`
- `model.generate`

This is how the orchestrator remains constrained even when model calls are dynamic.

## Extending the system

To add a built-in block:

1. Create a new specialist package under `agent/specialists/`.
2. Implement one or more `SpecialistAgent` subclasses.
3. Expose a `create_block()` factory that returns an `AgentBlock`.
4. Register the block through the Python package discovery process.

The block API is intentionally simple; `orchestrator.py` stays generic and does not require per-integration edits.

## Related docs

- [backend/README.md](../../README.md)
- [backend/BLOCKS.md](../../BLOCKS.md)
- [backend/src/agent/specialists/README.md](specialists/README.md)
- [backend/src/providers/README.md](../providers/README.md)
- [backend/src/repositories/README.md](../repositories/README.md)
- [backend/src/services/README.md](../services/README.md)
