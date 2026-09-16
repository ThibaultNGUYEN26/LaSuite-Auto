"""Errors shared by the orchestrator and specialist agents."""


class AgentError(RuntimeError):
    """Raised when the orchestrator cannot complete a request."""


class SpecialistAgentError(AgentError):
    """A specialist agent could not complete its delegated task."""


class DriveAPIError(SpecialistAgentError):
    """Drive could not return a usable response."""


class LocalFilesError(SpecialistAgentError):
    """A local-files operation could not be completed safely."""


class GristAPIError(SpecialistAgentError):
    """Grist could not complete a requested operation."""


class CodeExecutionError(SpecialistAgentError):
    """A code-execution operation could not be completed safely."""


class DataAnalysisError(SpecialistAgentError):
    """Tabular data could not be read or analyzed safely."""


class AlbertAPIError(AgentError):
    """Albert could not return a usable response."""
