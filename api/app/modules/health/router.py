from typing import Literal

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str


class ReadinessResponse(BaseModel):
    status: Literal["ok", "unavailable"]
    database: bool
    pgvector: bool


@router.get("", name="getHealth", summary="Liveness check")
async def get_health() -> HealthResponse:
    """Liveness: the process is up. Never touches the database."""
    return HealthResponse(status="ok", service="ask-my-portfolio-api")


@router.get(
    "/ready",
    name="getReadiness",
    summary="Readiness check",
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ReadinessResponse}},
)
async def get_readiness(request: Request, response: Response) -> ReadinessResponse:
    """Readiness: the database is reachable and the pgvector extension is installed."""
    engine: AsyncEngine = request.app.state.engine
    database = pgvector = False
    try:
        async with engine.connect() as conn:
            database = True
            result = await conn.execute(
                text("SELECT 1 FROM pg_extension WHERE extname = 'vector'"),
            )
            pgvector = result.scalar() is not None
    except Exception:  # any DB error means "not ready"; details go to the logs, not the client
        request.app.state.logger.exception("Readiness check failed")

    ready = database and pgvector
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadinessResponse(
        status="ok" if ready else "unavailable", database=database, pgvector=pgvector
    )
