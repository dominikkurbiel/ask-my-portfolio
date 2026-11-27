# API (FastAPI)

## Stack

Python 3.13 (managed by uv), FastAPI, Pydantic v2, pydantic-settings, SQLAlchemy 2 (async) with
psycopg 3, Alembic, pgvector. Tooling: ruff (lint + format), pyright (strict), pytest (+ pytest-asyncio,
httpx, testcontainers).

## Commands (run in `api/`)

```bash
uv run poe dev                            # database (docker compose) + migrations + API with reload on :8000
uv run poe check                          # format check, lint, pyright, tests (same as CI)
uv run poe format                         # format + auto-fix lint
uv run poe test                           # all tests (integration ones need Docker), except `model`
uv run poe test-model                     # tests with the real embedding model (~1 GB download once)
uv run poe migrate                        # alembic upgrade head
uv run poe openapi                        # refresh openapi.json for the web client
uv run pytest -m "not integration"        # fast unit tests only
uv run alembic revision --autogenerate -m "..."  # migration from model changes
uv add <pkg> / uv add --dev <pkg>         # never pip install; `uv run` syncs .venv by itself
```

Tasks are defined in `[tool.poe.tasks]` in `pyproject.toml` (poethepoet, like `scripts` in
package.json). Add a task there instead of documenting long commands.

## Structure: modular monolith

- `app/main.py` is the **composition root**: `create_app(settings)` builds the app, owns the lifespan
  (engine, clients) and wires modules together. Modules don't build their own dependencies.
- Features live in `app/modules/<name>/`. A module imports another one **only through its
  `__init__.py`** (its public API), never its internal files.
- Shared infrastructure: `app/config.py` (settings), `app/db/` (engine, `Base`).
- Every endpoint is under the `/api` prefix. Give each route an explicit `name="camelCase"`: it becomes
  the OpenAPI operation id and the name of the generated TS function/hook.

## Ports and adapters

External services (LLM, embeddings, GitHub, ...) are hidden behind a small interface (`typing.Protocol`)
in the module that needs them, with a real adapter and a fake for tests. Domain logic never imports
`anthropic`, `fastembed` etc. directly, so unit tests run without network and without cost.

## Code style

- Fully typed, pyright strict must pass; no `Any` unless a library forces it (then narrow it at once).
- `async` all the way for I/O; never call blocking I/O inside `async def` (ruff `ASYNC` rules).
- Request/response bodies are Pydantic models; return the model, not a dict.
- Settings only through `Settings` (env variables), never `os.environ` in modules.
- Errors: don't leak internals to clients; log the details, return a clear status/message.

## Database

- Each module owns its tables (models in `modules/<name>/models.py`, registered on `app.db.Base`).
- Change models → `alembic revision --autogenerate` → review the generated file → commit it.
  Never edit a migration that has been applied (pushed); add a new one.

## Tests

- `tests/` mirrors `app/`. Unit tests use fakes; `tests/integration/` uses a real PostgreSQL + pgvector
  via testcontainers (mark with `pytest.mark.integration`).
- Test the app through `create_app(Settings(...))` + `httpx.AsyncClient(transport=ASGITransport(app))`
  inside `app.router.lifespan_context(app)`.
