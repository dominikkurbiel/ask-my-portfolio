from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def create_engine(database_url: str) -> AsyncEngine:
    # pool_pre_ping: check a pooled connection before using it (survives DB restarts)
    return create_async_engine(database_url, pool_pre_ping=True)
