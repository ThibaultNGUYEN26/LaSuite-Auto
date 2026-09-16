"""Capability-block manifests, discovery, and registry composition."""

from __future__ import annotations

import importlib
import importlib.util
import pkgutil
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from importlib import metadata
from typing import Literal

from agent.base import SpecialistAgent
from agent.errors import AgentError
from agent.registry import AgentRegistry


BLOCK_ENTRY_POINT_GROUP = "lasuite_automations.blocks"
BLOCK_FACTORY_NAME = "create_block"
SideEffect = Literal[
    "none",
    "local_read",
    "local_write",
    "external_read",
    "external_write",
    "code_execution",
]


class BlockLoadError(AgentError):
    """A capability block could not be discovered or constructed."""


@dataclass(frozen=True)
class ConfigRequirement:
    """Configuration declared by a block for validation and future injection."""

    name: str
    required: bool = False
    secret: bool = False
    description: str = ""


@dataclass(frozen=True)
class ArtifactContract:
    """A typed value a capability can consume or produce."""

    kind: str
    media_types: tuple[str, ...] = ()
    description: str = ""


@dataclass(frozen=True)
class CapabilityManifest:
    """Policy and interoperability metadata for one model-facing agent."""

    name: str
    description: str
    side_effect: SideEffect = "none"
    permissions: tuple[str, ...] = ()
    accepts: tuple[ArtifactContract, ...] = ()
    produces: tuple[ArtifactContract, ...] = ()
    confirmation_required: bool = False


@dataclass(frozen=True)
class WorkflowManifest:
    """A reliable, reusable route across named capabilities."""

    name: str
    description: str
    capabilities: tuple[str, ...]


@dataclass(frozen=True)
class AgentBlock:
    """A named, independently installable group of specialist capabilities."""

    name: str
    agents: tuple[SpecialistAgent, ...]
    description: str = ""
    capabilities: tuple[CapabilityManifest, ...] = ()
    required_config: tuple[ConfigRequirement, ...] = ()
    permissions: tuple[str, ...] = ()
    workflows: tuple[WorkflowManifest, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("A block must have a name")
        if not self.agents:
            raise ValueError(f"Block {self.name!r} must provide at least one agent")
        if not all(isinstance(agent, SpecialistAgent) for agent in self.agents):
            raise TypeError(f"Block {self.name!r} contains an invalid agent")

        agent_names = [agent.name for agent in self.agents]
        if len(agent_names) != len(set(agent_names)):
            raise ValueError(f"Block {self.name!r} contains duplicate agent names")
        if self.capabilities:
            capability_names = [capability.name for capability in self.capabilities]
            if set(capability_names) != set(agent_names):
                raise ValueError(
                    f"Block {self.name!r} capability names must match its agents"
                )

    def capability_catalog(self) -> tuple[CapabilityManifest, ...]:
        """Return explicit metadata, or safe defaults for legacy contributors."""
        if self.capabilities:
            return self.capabilities
        return tuple(
            CapabilityManifest(name=agent.name, description=agent.description)
            for agent in self.agents
        )

    def summary(self) -> dict[str, object]:
        """Compact metadata used during first-stage block selection."""
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": [
                {
                    "name": capability.name,
                    "description": capability.description,
                    "side_effect": capability.side_effect,
                    "accepts": [artifact.kind for artifact in capability.accepts],
                    "produces": [artifact.kind for artifact in capability.produces],
                }
                for capability in self.capability_catalog()
            ],
            "workflows": [
                {
                    "name": workflow.name,
                    "description": workflow.description,
                    "capabilities": list(workflow.capabilities),
                }
                for workflow in self.workflows
            ],
        }


BlockFactory = Callable[[], AgentBlock]


class BlockRegistry:
    """Catalog of blocks that can expose only the capabilities relevant to a task."""

    def __init__(
        self,
        blocks: Iterable[AgentBlock] = (),
        *,
        allowed_permissions: Iterable[str] = ("*",),
    ) -> None:
        self._blocks: dict[str, AgentBlock] = {}
        self._allowed_permissions = frozenset(allowed_permissions)
        for block in blocks:
            if block.name in self._blocks:
                raise BlockLoadError(f"Duplicate block name: {block.name}")
            self._blocks[block.name] = block

    @classmethod
    def discover(
        cls, *, allowed_permissions: Iterable[str] = ("*",)
    ) -> "BlockRegistry":
        return cls(
            discover_blocks(),
            allowed_permissions=allowed_permissions,
        )

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(self._blocks)

    def catalog(
        self, block_names: Iterable[str] | None = None
    ) -> list[dict[str, object]]:
        selected_names = self.names if block_names is None else tuple(block_names)
        unknown = sorted(set(selected_names) - set(self._blocks))
        if unknown:
            raise BlockLoadError(f"Unknown capability blocks: {', '.join(unknown)}")
        return [self._blocks[name].summary() for name in selected_names]

    def agent_registry(self, block_names: Iterable[str] | None = None) -> AgentRegistry:
        selected_names = self.names if block_names is None else tuple(block_names)
        unknown = sorted(set(selected_names) - set(self._blocks))
        if unknown:
            raise BlockLoadError(f"Unknown capability blocks: {', '.join(unknown)}")
        if "*" not in self._allowed_permissions:
            denied = sorted(
                {
                    permission
                    for name in selected_names
                    for permission in self._blocks[name].permissions
                    if permission not in self._allowed_permissions
                }
            )
            if denied:
                raise BlockLoadError(
                    "Selected blocks require permissions that are not allowed: "
                    + ", ".join(denied)
                )
        try:
            return AgentRegistry(
                agent
                for name in selected_names
                for agent in self._blocks[name].agents
            )
        except ValueError as exc:
            raise BlockLoadError(f"Could not register capability blocks: {exc}") from exc


def _load_factory(module_name: str) -> BlockFactory:
    module = importlib.import_module(module_name)
    factory = getattr(module, BLOCK_FACTORY_NAME, None)
    if not callable(factory):
        raise BlockLoadError(
            f"Block module {module_name!r} must expose {BLOCK_FACTORY_NAME}()"
        )
    return factory


def _build_block(factory: BlockFactory, source: str) -> AgentBlock:
    try:
        block = factory()
    except Exception as exc:
        raise BlockLoadError(f"Could not load block from {source}: {exc}") from exc
    if not isinstance(block, AgentBlock):
        raise BlockLoadError(f"Block factory {source} did not return an AgentBlock")
    return block


def discover_builtin_blocks() -> list[AgentBlock]:
    """Load every ``agent.specialists.<name>.block`` module that exists."""
    from agent import specialists

    blocks: list[AgentBlock] = []
    packages = sorted(
        module.name
        for module in pkgutil.iter_modules(specialists.__path__)
        if module.ispkg and not module.name.startswith("_")
    )
    for package_name in packages:
        module_name = f"agent.specialists.{package_name}.block"
        if importlib.util.find_spec(module_name) is None:
            continue
        blocks.append(_build_block(_load_factory(module_name), module_name))
    return blocks


def discover_external_blocks() -> list[AgentBlock]:
    """Load blocks contributed by installed Python packages."""
    discovered = metadata.entry_points()
    entry_points: Iterable[metadata.EntryPoint]
    if hasattr(discovered, "select"):
        entry_points = discovered.select(group=BLOCK_ENTRY_POINT_GROUP)
    else:  # pragma: no cover
        entry_points = discovered.get(BLOCK_ENTRY_POINT_GROUP, ())

    blocks: list[AgentBlock] = []
    for entry_point in sorted(entry_points, key=lambda item: item.name):
        try:
            factory = entry_point.load()
        except Exception as exc:
            raise BlockLoadError(
                f"Could not import external block {entry_point.name!r}: {exc}"
            ) from exc
        if not callable(factory):
            raise BlockLoadError(
                f"External block {entry_point.name!r} is not a factory"
            )
        blocks.append(_build_block(factory, f"entry point {entry_point.name!r}"))
    return blocks


def discover_blocks() -> list[AgentBlock]:
    return [*discover_builtin_blocks(), *discover_external_blocks()]


def build_agent_registry(blocks: Iterable[AgentBlock] | None = None) -> AgentRegistry:
    """Compatibility helper returning all capabilities in a flat registry."""
    registry = BlockRegistry.discover() if blocks is None else BlockRegistry(blocks)
    return registry.agent_registry()
