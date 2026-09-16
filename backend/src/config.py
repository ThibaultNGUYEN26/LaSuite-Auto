import os
from pathlib import Path
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
    albert_vision_model: str | None = os.environ.get("ALBERT_VISION_MODEL") or None
    drive_base_url: str = os.environ.get("DRIVE_BASE_URL", "http://localhost:8071")
    drive_session_id: str | None = os.environ.get("DRIVE_SESSION_ID") or None
    drive_csrf_token: str | None = os.environ.get("DRIVE_CSRF_TOKEN") or None
    drive_upload_acl: str | None = os.environ.get("DRIVE_UPLOAD_ACL") or None
    drive_max_create_bytes: int = int(
        os.environ.get("DRIVE_MAX_CREATE_BYTES", str(1024 * 1024))
    )
    drive_max_download_bytes: int = int(
        os.environ.get("DRIVE_MAX_DOWNLOAD_BYTES", str(20 * 1024 * 1024))
    )
    pdf_max_text_characters: int = int(
        os.environ.get("PDF_MAX_TEXT_CHARACTERS", "80000")
    )
    local_files_root: Path = Path(
        os.environ.get("LOCAL_FILES_ROOT", str(Path.home()))
    ).expanduser()
    local_files_max_read_bytes: int = int(
        os.environ.get("LOCAL_FILES_MAX_READ_BYTES", str(20 * 1024 * 1024))
    )
    local_files_max_create_bytes: int = int(
        os.environ.get("LOCAL_FILES_MAX_CREATE_BYTES", str(1024 * 1024))
    )
    image_max_read_bytes: int = int(
        os.environ.get("IMAGE_MAX_READ_BYTES", str(10 * 1024 * 1024))
    )
    workflows_db_path: str = os.environ.get("WORKFLOWS_DB_PATH", "./data/workflows.db")

    # Full URL (protocol + host + port) the backend binds to and that the
    # frontend uses to reach it. Shared with the frontend via the same
    # BACKEND_URL env var name so both sides agree on where the backend lives,
    # even when it isn't running on the same machine as the frontend.
    backend_url: str = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
    _parsed_backend_url = urlparse(backend_url)
    host: str = _parsed_backend_url.hostname or "127.0.0.1"
    port: int = _parsed_backend_url.port or 8000


settings = Settings()
