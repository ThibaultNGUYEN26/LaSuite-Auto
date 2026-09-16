"""Discover Grist workspaces available to the configured user."""

from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import GristAPIError
from services.grist import list_grist_workspaces


class GristListWorkspacesAgent(SpecialistAgent):
    name = "grist_list_workspaces"
    description = (
        "List the Grist workspaces and documents accessible to the configured user. "
        "Use this to find a workspace ID before importing a CSV when no default "
        "workspace is configured or the user names a different workspace."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    }

    def __init__(self, base_url: str, api_key: str | None, *, org_id: str) -> None:
        self.base_url = base_url
        self.api_key = api_key or ""
        self.org_id = org_id

    def execute(
        self, arguments: dict[str, Any], context: DelegationContext
    ) -> dict[str, Any]:
        del context
        if arguments:
            raise GristAPIError("grist_list_workspaces does not accept arguments")
        return list_grist_workspaces(
            self.base_url,
            self.api_key,
            org_id=self.org_id,
        )
