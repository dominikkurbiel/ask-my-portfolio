"""Database infrastructure shared by all modules."""

from app.db.base import Base
from app.db.engine import create_engine

__all__ = ["Base", "create_engine"]
