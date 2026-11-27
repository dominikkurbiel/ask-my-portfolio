"""Liveness and readiness checks (used by Docker / Coolify and the web app)."""

from app.modules.health.router import router

__all__ = ["router"]
