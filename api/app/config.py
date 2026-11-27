from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


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

    # Local multilingual embedding model (fastembed). Changing it means re-indexing everything.
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    # Where downloaded models are kept (outside the repo, survives restarts)
    embedding_cache_dir: Path = Path.home() / ".cache" / "ask-my-portfolio" / "fastembed"

    # Markdown content to index (CV, about me). The real content/ folder is private and
    # git-ignored; tests and CI point this at the public content.example/ folder.
    content_dir: Path = REPO_ROOT / "content"


@lru_cache
def get_settings() -> Settings:
    return Settings()
