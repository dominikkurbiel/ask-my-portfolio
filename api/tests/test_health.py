from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    # Points at a port where nothing listens: readiness must fail gracefully, not crash
    app = create_app(
        Settings(environment="test", database_url="postgresql+psycopg://x:x@127.0.0.1:1/x")
    )
    async with (
        app.router.lifespan_context(app),
        AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client,
    ):
        yield client


async def test_health_is_ok(client: AsyncClient) -> None:
    response = await client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ask-my-portfolio-api"}


async def test_readiness_reports_unavailable_database(client: AsyncClient) -> None:
    response = await client.get("/api/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "unavailable", "database": False, "pgvector": False}
