"""Application settings, read from environment variables or a .env file."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(REPO_ROOT / ".env", ".env"), env_file_encoding="utf-8", extra="ignore"
    )

    database_url: str = "postgresql+psycopg://stj:stj@localhost:5432/stj"
    companies_file: Path = REPO_ROOT / "data" / "companies.yaml"

    collector_user_agent: str = (
        "SaudiTechJobsBot/0.1 (+https://github.com/Abdulaziz20245/Saudi-Tech-Jobs)"
    )
    collector_rate_limit_per_sec: float = 1.0
    collector_timeout_sec: float = 30.0

    cors_origins: str = "http://localhost:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()
