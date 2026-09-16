"""Portable typed references exchanged between capability blocks."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Artifact(BaseModel):
    """A reference to data, not the data itself, safe for model tool messages."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: str = Field(min_length=1)
    location: Literal["local", "drive", "remote", "memory"]
    reference: str = Field(min_length=1)
    media_type: str = "application/octet-stream"
    name: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def tool_value(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
