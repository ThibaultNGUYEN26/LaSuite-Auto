"""Bounded in-memory storage for artifacts exchanged between blocks."""

from __future__ import annotations

from collections import OrderedDict
from copy import deepcopy
from threading import RLock
from typing import Any
from uuid import uuid4

from agent.artifacts import Artifact


class ArtifactNotFoundError(KeyError):
    """An in-memory artifact is unknown or no longer retained."""


class MemoryArtifactStore:
    """Keep bounded structured results available during orchestration."""

    def __init__(self, *, max_items: int = 128) -> None:
        if max_items < 1:
            raise ValueError("max_items must be positive")
        self.max_items = max_items
        self._items: OrderedDict[str, tuple[str, Any]] = OrderedDict()
        self._lock = RLock()

    def put(
        self,
        payload: Any,
        *,
        kind: str,
        media_type: str,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Artifact:
        reference = str(uuid4())
        with self._lock:
            self._items[reference] = (kind, deepcopy(payload))
            while len(self._items) > self.max_items:
                self._items.popitem(last=False)
        return Artifact(
            kind=kind,
            location="memory",
            reference=reference,
            media_type=media_type,
            name=name,
            metadata=metadata or {},
        )

    def get(self, artifact: Artifact, *, expected_kind: str) -> Any:
        if artifact.location != "memory" or artifact.kind != expected_kind:
            raise ArtifactNotFoundError("The artifact has the wrong type or location")
        with self._lock:
            stored = self._items.get(artifact.reference)
            if stored is None or stored[0] != expected_kind:
                raise ArtifactNotFoundError(
                    "The analysis result is no longer available; analyze the data again"
                )
            self._items.move_to_end(artifact.reference)
            return deepcopy(stored[1])

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


memory_artifact_store = MemoryArtifactStore()
