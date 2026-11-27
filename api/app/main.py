import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute

from app.config import Settings, get_settings
from app.db import create_engine
from app.modules import health


def _operation_id(route: APIRoute) -> str:
    # Clean OpenAPI operation ids ("getHealth") -> clean names in the generated TS client
    return route.name


def create_app(settings: Settings | None = None) -> FastAPI:
    """Composition root: builds the app and wires the modules together."""
    settings = settings or get_settings()
    logging.basicConfig(level=settings.log_level)
    logger = logging.getLogger("app")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        engine = create_engine(settings.database_url)
        app.state.engine = engine
        logger.info("API started (%s)", settings.environment)
        yield
        await engine.dispose()

    app = FastAPI(
        title="Ask my portfolio API",
        version="0.1.0",
        lifespan=lifespan,
        generate_unique_id_function=_operation_id,
        # Interactive docs only outside production
        docs_url="/api/docs" if settings.environment != "production" else None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
    )
    app.state.settings = settings
    app.state.logger = logger

    # Every endpoint lives under /api: the web app and the API share one origin
    api = APIRouter(prefix="/api")
    api.include_router(health.router)
    app.include_router(api)

    return app


app = create_app()
