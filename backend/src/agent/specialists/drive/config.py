"""Drive public-configuration specialist."""

from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import get_drive_config


class DriveConfigAgent(SpecialistAgent):
    name = "drive_get_config"
    description = (
        "Read the current public configuration of the La Suite Drive instance. "
        "Use this only for Drive languages, feature flags, environment, and public URLs."
    )
    parameters: dict[str, Any] = {
        "type": "object", "properties": {}, "additionalProperties": False
    }

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def execute(self, arguments: dict[str, Any], context: DelegationContext) -> dict[str, Any]:
        del context
        if arguments:
            raise DriveAPIError("drive_get_config does not accept arguments")
        return get_drive_config(self.base_url)
