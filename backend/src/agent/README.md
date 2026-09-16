# Capability blocks

The orchestrator is a domain-agnostic reasoning loop. It knows how to select,
chain, and evaluate capabilities, but it does not import or name Drive, local
files, Grist, Python, or any future integration. `agent.runtime` discovers
blocks, flattens their specialist agents into `AgentRegistry`, and gives that
registry to the orchestrator.

The runtime performs two-stage routing: the first model call receives only
compact block manifests, then the planning loop receives detailed schemas only
for the selected blocks. Typed `Artifact` references connect outputs from one
block to inputs of another. See `backend/BLOCKS.md` for the complete contributor
contract.

Specialists are grouped by domain instead of being placed beside the
orchestrator:

```text
agent/
  blocks.py
  orchestrator.py
  runtime.py
  specialists/
    drive/
      block.py
      config.py
      list_items.py
      read_image.py
      read_pdf.py
    local_files/
      block.py
      create_file.py
      list_items.py
      read_image.py
      read_pdf.py
services/
  drive.py
  image.py
  local_files.py
  pdf.py
```

A block owns an integration boundary and constructs one or more model-facing
agents. An agent owns one capability and its input validation. A service owns
reusable API details. The brain only receives the resulting JSON schemas.

## Reading a Drive PDF

The coordinator now advertises three Drive tools:

- `drive_list_items` discovers files recursively and returns their UUIDs.
- `drive_read_pdf` downloads one UUID with the authenticated Drive session and
  reads its selectable text entirely in backend memory.
- `drive_get_config` reads public instance configuration.

For a request such as "Summarize the PDF named budget.pdf in my Drive", Albert
can first call `drive_list_items`, select the matching PDF UUID, then call
`drive_read_pdf`. Scanned image-only PDFs return an explicit no-extractable-text
error.

## Reading a local PDF

`local_files_list_items` lists any relative directory below the configured
`LOCAL_FILES_ROOT` (the current user's home folder by default) and returns safe
relative paths. For example, the coordinator can select `Downloads`, `Documents`,
or `Desktop` with the `directory` argument.
`local_files_read_pdf` accepts one of those relative paths, reads the PDF into
memory, and uses the same text extractor as the Drive specialist. Absolute
paths and paths that escape the configured root are rejected.

## Reading images

`drive_read_image` and `local_files_read_image` load PNG, JPEG, GIF, or WebP
bytes into backend memory and send them directly to an Albert
`image-text-to-text` model. The text-generation model remains the coordinator;
it does not inspect the pixels itself. Set `ALBERT_VISION_MODEL` to a canonical
vision model ID, or leave it empty to select the first compatible model from
Albert's live catalogue. Only the textual analysis is returned to the
orchestrator; raw image data is not copied into tool results.

## Creating local files

`local_files_create_file` creates a new UTF-8 text file with a requested
extension inside an existing directory under `LOCAL_FILES_ROOT`. It is exposed
only for explicit file-creation requests. Existing files are never overwritten,
directories are not created implicitly, and content size is bounded by
`LOCAL_FILES_MAX_CREATE_BYTES`.

## Creating Drive files

`drive_create_file` uploads a new UTF-8 text file either to the top of My Files
or to a folder selected by UUID. It follows Drive's create, signed upload, and
upload-complete sequence. Configure `DRIVE_CSRF_TOKEN` from the same authenticated
browser session as `DRIVE_SESSION_ID`; `DRIVE_MAX_CREATE_BYTES` bounds content size.
The storage ACL is read from Drive automatically, unless `DRIVE_UPLOAD_ACL` overrides it.
The specialist creates text content with extensions such as `.txt`, `.md`, `.csv`,
or `.json`; changing an extension does not generate a binary PDF or DOCX document.

`drive_create_files` creates several text files in one bounded batch, so a request
for many files does not consume one orchestration round per file. The entire batch
is validated before the first upload, and the result reports each success and
failure. `DRIVE_MAX_BATCH_FILES` controls the maximum number of files per batch.

`drive_upload_file` handles existing local files whose exact bytes must be
preserved, including PDFs, images, archives, office documents, and arbitrary
binary formats. Its source path is restricted to `LOCAL_FILES_ROOT`, it can
target a Drive folder UUID, and uploads are bounded by `DRIVE_MAX_UPLOAD_BYTES`.

## Importing CSV files into Grist

`grist_list_workspaces` discovers available destination workspaces and their
documents. `grist_import_csv` creates a new Grist document from UTF-8 CSV text,
a local CSV below `LOCAL_FILES_ROOT`, or a CSV downloaded from La Suite Drive.
Set `GRIST_API_KEY`, `GRIST_ORG_ID`, and optionally `GRIST_WORKSPACE_ID` in
`.env`. Imports are bounded by `GRIST_MAX_IMPORT_BYTES` and are performed only
after an explicit user request; existing Grist documents are not replaced.

## Routing flow

1. `OrchestratorAgent` sends the conversation and registered tool definitions
   to Albert.
2. Albert selects the specialist whose description and parameter schema match
   the user's intent.
3. `AgentRegistry` parses the arguments and invokes that specialist.
4. The structured result is returned to Albert, which may delegate another step
   or produce the final response.

## Adding a built-in block

Create a package below `agent/specialists`, implement one or more
`SpecialistAgent` classes, then expose a `block.py`. Discovery is automatic;
there is no central list and `orchestrator.py` must not be modified.

```python
from typing import Any

from agent.base import DelegationContext, SpecialistAgent


class DocsSearchAgent(SpecialistAgent):
    name = "docs_search"
    description = "Search documents available in the configured Docs service."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
        },
        "required": ["query"],
        "additionalProperties": False,
    }

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        return {"results": []}
```

```python
# agent/specialists/docs/block.py
from agent.blocks import AgentBlock
from agent.specialists.docs.search import DocsSearchAgent


def create_block() -> AgentBlock:
    return AgentBlock(
        name="docs",
        description="Search and manage collaborative documents.",
        agents=(DocsSearchAgent(),),
    )
```

At the next backend start, `agent.blocks.discover_builtin_blocks()` finds the
package and advertises its agents to the brain.

## Publishing an external block

An independently maintained Python package can expose the same zero-argument
factory through the `lasuite_automations.blocks` entry-point group:

```toml
[project.entry-points."lasuite_automations.blocks"]
docs = "my_lasuite_docs.block:create_block"
```

Installing that package into the backend environment is enough. The core
repository, runtime, and orchestrator require no changes. Block names and agent
names must be globally unique; startup fails clearly when a collision exists.

Each block must enforce its own authentication, path boundaries, permissions,
and mutation safeguards. It must not trust model-provided identifiers blindly.
Return structured results and errors rather than a prewritten assistant response
so the brain can combine several blocks in one request.
