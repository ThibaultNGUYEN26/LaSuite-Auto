"""Grist capability block."""

from agent.blocks import (
    AgentBlock,
    ArtifactContract,
    CapabilityManifest,
    ConfigRequirement,
    WorkflowManifest,
)
from agent.specialists.grist import GristImportCsvAgent, GristListWorkspacesAgent
from config import settings


def create_block() -> AgentBlock:
    return AgentBlock(
        name="grist",
        description="Discover Grist workspaces and import CSV data.",
        required_config=(
            ConfigRequirement("GRIST_BASE_URL", required=True),
            ConfigRequirement("GRIST_API_KEY", required=True, secret=True),
        ),
        permissions=("grist.read", "grist.write"),
        capabilities=(
            CapabilityManifest(
                "grist_list_workspaces",
                "List accessible Grist workspaces and documents.",
                side_effect="external_read",
                permissions=("grist.read",),
            ),
            CapabilityManifest(
                "grist_import_csv",
                "Create a Grist document from a CSV artifact.",
                side_effect="external_write",
                permissions=("grist.write",),
                accepts=(ArtifactContract("file", ("text/csv",)),),
                produces=(ArtifactContract("grist_document"),),
            ),
        ),
        workflows=(
            WorkflowManifest(
                "grist.import_csv",
                "Choose a workspace and import validated CSV data.",
                ("grist_list_workspaces", "grist_import_csv"),
            ),
        ),
        agents=(
            GristListWorkspacesAgent(
                settings.grist_base_url,
                settings.grist_api_key,
                org_id=settings.grist_org_id,
            ),
            GristImportCsvAgent(
                settings.grist_base_url,
                settings.grist_api_key,
                org_id=settings.grist_org_id,
                workspace_id=settings.grist_workspace_id,
                local_files_root=settings.local_files_root,
                drive_base_url=settings.drive_base_url,
                drive_session_id=settings.drive_session_id,
                max_import_bytes=settings.grist_max_import_bytes,
            ),
        ),
    )
