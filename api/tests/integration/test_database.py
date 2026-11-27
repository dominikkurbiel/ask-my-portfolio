"""Runs migrations against a real PostgreSQL + pgvector started in Docker (testcontainers)."""

from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from testcontainers.community.postgres import PostgresContainer

from alembic import command
from app.config import Settings
from app.main import create_app

pytestmark = pytest.mark.integration

API_DIR = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def database_url() -> Iterator[str]:
    with PostgresContainer("pgvector/pgvector:pg17", driver="psycopg") as postgres:
        url = postgres.get_connection_url()
        config = Config(API_DIR / "alembic.ini")
        config.set_main_option("script_location", str(API_DIR / "alembic"))
        config.set_main_option("sqlalchemy.url", url)
        config.attributes["configure_logger"] = False
        command.upgrade(config, "head")
        yield url


@pytest.fixture
async def client(database_url: str) -> AsyncIterator[AsyncClient]:
    app = create_app(Settings(environment="test", database_url=database_url))
    async with (
        app.router.lifespan_context(app),
        AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client,
    ):
        yield client


async def test_ready_after_migrations(client: AsyncClient) -> None:
    response = await client.get("/api/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": True, "pgvector": True}
