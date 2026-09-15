"""Errors shared by the orchestrator and specialist agents."""


class AgentError(RuntimeError):
    """Raised when the orchestrator cannot complete a request."""


class SpecialistAgentError(AgentError):
    """A specialist agent could not complete its delegated task."""


class DriveAPIError(SpecialistAgentError):
    """Drive could not return a usable response."""


class AlbertAPIError(AgentError):
    """Albert could not return a usable response."""
