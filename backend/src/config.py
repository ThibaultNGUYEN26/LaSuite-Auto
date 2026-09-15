import os
from pathlib import Path


def load_env_file(path: Path | None = None) -> None:
    """Load simple KEY=VALUE entries without overriding shell variables."""
    env_path = path or Path(__file__).resolve().parents[1] / ".env"
    if not env_path.is_file():
        return

    for line_number, raw_line in enumerate(
        env_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").lstrip()
        key, separator, value = line.partition("=")
        key = key.strip()
        if not separator or not key.isidentifier():
            raise ValueError(f"Invalid .env entry on line {line_number}")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        os.environ.setdefault(key, value)


load_env_file()


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


settings = Settings()
