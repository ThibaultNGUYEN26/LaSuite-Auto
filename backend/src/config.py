import os
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Which provider/model is active, loaded from environment/settings."""

    provider: str = os.environ.get("AUTO_PROVIDER", "echo")
    cors_origins: list[str] = os.environ.get("AUTO_CORS_ORIGINS", "*").split(",")
    albert_api_key: str | None = os.environ.get("ALBERT_API_KEY")
    albert_base_url: str = os.environ.get(
        "ALBERT_BASE_URL", "https://albert.api.etalab.gouv.fr/v1"
    )
    albert_model: str | None = os.environ.get("ALBERT_MODEL") or None
    drive_base_url: str = os.environ.get("DRIVE_BASE_URL", "http://localhost:8071")

    # Full URL (protocol + host + port) the backend binds to and that the
    # frontend uses to reach it. Shared with the frontend via the same
    # BACKEND_URL env var name so both sides agree on where the backend lives,
    # even when it isn't running on the same machine as the frontend.
    backend_url: str = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
    _parsed_backend_url = urlparse(backend_url)
    host: str = _parsed_backend_url.hostname or "127.0.0.1"
    port: int = _parsed_backend_url.port or 8000


settings = Settings()
