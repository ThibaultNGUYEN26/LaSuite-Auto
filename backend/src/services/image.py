"""Image validation and Albert vision analysis."""

from __future__ import annotations

import base64
from typing import Any, Protocol

from agent.errors import AlbertAPIError, SpecialistAgentError
from providers.albert import AlbertClient


def detect_image_mime(data: bytes) -> str:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    raise SpecialistAgentError(
        "Unsupported image format. Supported formats are PNG, JPEG, GIF, and WebP."
    )


class ImageAnalyzer(Protocol):
    def analyze(self, data: bytes, question: str) -> dict[str, Any]: ...


class AlbertImageAnalyzer:
    """Lazily call an Albert image-text-to-text model with an in-memory image."""

    def __init__(
        self,
        api_key: str | None,
        *,
        base_url: str,
        requested_model: str | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.requested_model = requested_model
        self._client: AlbertClient | None = None
        self._model: str | None = None

    def analyze(self, data: bytes, question: str) -> dict[str, Any]:
        if not self.api_key:
            raise AlbertAPIError("Set ALBERT_API_KEY before reading an image")
        mime_type = detect_image_mime(data)
        if self._client is None:
            self._client = AlbertClient(self.api_key, base_url=self.base_url)
        if self._model is None:
            self._model = self._client.resolve_model_by_type(
                "image-text-to-text",
                self.requested_model,
                setting_name="ALBERT_VISION_MODEL",
            )
        encoded = base64.b64encode(data).decode("ascii")
        answer = self._client.image_completion(
            model=self._model,
            prompt=question,
            data_url=f"data:{mime_type};base64,{encoded}",
        )
        return {"answer": answer, "mime_type": mime_type, "model": self._model}
