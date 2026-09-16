# Building capability blocks

A block is an independently discoverable integration. The orchestrator never
imports blocks directly. At startup, the runtime discovers built-in block
packages and installed Python entry points, then uses compact manifests to
select only the relevant blocks for each conversation.

## Minimal layout

```text
agent/specialists/docs/
  __init__.py
  block.py
  create_document.py
  read_document.py
```

Each tool implements `SpecialistAgent`. `block.py` exposes a zero-argument
`create_block()` factory:

```python
from agent.blocks import (
    AgentBlock,
    ArtifactContract,
    CapabilityManifest,
    ConfigRequirement,
    WorkflowManifest,
)
from agent.specialists.docs import DocsCreateAgent, DocsReadAgent


def create_block() -> AgentBlock:
    return AgentBlock(
        name="docs",
        description="Create and read collaborative documents.",
        required_config=(
            ConfigRequirement("DOCS_BASE_URL", required=True),
            ConfigRequirement("DOCS_API_KEY", required=True, secret=True),
        ),
        permissions=("docs.read", "docs.write"),
        capabilities=(
            CapabilityManifest(
                name="docs_read",
                description="Read one collaborative document.",
                side_effect="external_read",
                permissions=("docs.read",),
                accepts=(ArtifactContract("document_reference"),),
                produces=(ArtifactContract("text", ("text/plain",)),),
            ),
            CapabilityManifest(
                name="docs_create",
                description="Create a collaborative document.",
                side_effect="external_write",
                permissions=("docs.write",),
                accepts=(ArtifactContract("text", ("text/plain", "text/markdown")),),
                produces=(ArtifactContract("document"),),
                confirmation_required=True,
            ),
        ),
        workflows=(
            WorkflowManifest(
                name="docs.publish",
                description="Create and verify a collaborative document.",
                capabilities=("docs_create", "docs_read"),
            ),
        ),
        agents=(DocsReadAgent(), DocsCreateAgent()),
    )
```

Capability names must exactly match the names of the supplied agents. Block and
agent names are globally unique.

## Typed artifacts

Tools should return an `artifact` whenever they create or locate reusable data:

```python
from agent.artifacts import Artifact

artifact = Artifact(
    kind="file",
    location="remote",
    reference="document-id",
    media_type="text/markdown",
    name="report.md",
)

return {"status": "created", "artifact": artifact.tool_value()}
```

Consumers accept that object rather than depending on another block's private
response format. Keep artifacts small: they are references and metadata, not
raw file bytes.

## External packages

Publish the factory through a Python package entry point:

```toml
[project.entry-points."lasuite_automations.blocks"]
docs = "my_lasuite_docs.block:create_block"
```

After the package is installed in the backend environment, restarting the
backend is enough to discover it. No core source file or system prompt changes
are required.

## Selection and workflows

The first model pass sees only compact block manifests. It selects every block
needed for the source, transformation, and destination of the request. The
planning pass then sees only the selected blocks' detailed tool schemas.

`WorkflowManifest` declares a dependable known sequence. It is routing metadata,
not a hard-coded replacement for reasoning: the orchestrator may still construct
a different plan when the request requires one.

## Permissions

Every block and capability declares permissions and side effects. Operators can
restrict enabled permissions with:

```env
AUTO_ALLOWED_BLOCK_PERMISSIONS=docs.read,docs.write,local.read
```

The registry refuses a selected block whose declared permissions are not in the
allowlist. `*` enables all permissions and is intended for local development.

This policy controls advertisement and dispatch, but Python entry points execute
inside the backend process. Only install trusted in-process packages. Supporting
untrusted community code requires a separate process, container, or remote/MCP
boundary; manifest declarations alone are not a security sandbox.

## Contributor rules

- Keep authentication and API behavior inside the block or its services.
- Never import the block from `agent/orchestrator.py` or `agent/runtime.py`.
- Describe capabilities precisely enough for block selection.
- Declare every credential, permission, side effect, accepted artifact, and
  produced artifact.
- Require explicit user intent for mutations and destructive actions.
- Return JSON-serializable structured results.
- Add discovery, policy, and behavior tests.
