from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration read from environment variables (and a .env file in development)."""

    model_config = SettingsConfigDict(
        # api/.env first, then the repo root .env (shared with docker compose)
        env_file=(".env", "../.env"),
        extra="ignore",
    )

    environment: Literal["development", "test", "production"] = "development"
    database_url: str = "postgresql+psycopg://portfolio:portfolio@localhost:5434/ask_my_portfolio"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
