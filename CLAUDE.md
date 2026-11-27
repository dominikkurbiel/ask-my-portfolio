# Ask my portfolio

A public RAG assistant: recruiters ask about my work and get streamed answers with citations to my CV,
READMEs and lines of code on GitHub. Portfolio project: code quality, clear history and measurable
quality (evals) matter more than shipping fast.

## Repository

- `api/`: Python 3.13, FastAPI. Rules in `api/CLAUDE.md`.
- `web/`: Next.js 16, TanStack Query, client generated from OpenAPI. Rules in `web/CLAUDE.md`.
- `docker-compose.yml`: PostgreSQL 17 + pgvector for development (host port 5434).
- `.github/workflows/ci.yml`: must stay green.
- `content/`: the real CV and about-me markdown. **Private: git-ignored, never commit it**, never copy
  its text into code, tests, fixtures or docs. It reaches the server through a deploy step.
- `content.example/`: public, fictional sample content (Jane Doe) for tests, CI and local runs.
  Tests must use it (or inline fixtures), never `content/`. Point the app at it with `CONTENT_DIR`.
- Planned: `evals/` (test questions), `sources.yaml` (repos to index).

## Commands

```bash
cd api && uv run poe dev     # database + migrations + API on :8000 (docs: /api/docs)
cd web && pnpm dev           # web on :3001, forwards /api/* to the API
cd api && uv run poe check   # everything CI checks on the API (list all tasks: uv run poe)
```

## Architecture (whole system)

- **Same origin:** the browser only calls `/api/*` on the web origin. Next.js rewrites it to FastAPI in
  development; the reverse proxy does it in production. No CORS; cookies stay simple.
- **API contract = OpenAPI.** FastAPI is the source of truth. After changing an endpoint or schema:
  `cd api && uv run python -m scripts.export_openapi`, then `cd web && pnpm api:generate`, and commit
  both `api/openapi.json` and `web/src/lib/api/generated/`. CI fails if they are out of date.
- **Retrieved content is data, never instructions** (prompt injection): CV, READMEs and code are
  passed to the model as documents, and nothing inside them can change the assistant's rules.
- **Every LLM call goes through guardrails and is logged** (tokens, cost, timings) — no exceptions.
- **Never put personal contact data** (phone, e-mail, address) into indexed content or logs; visitors'
  IPs are stored only as hashes.

## Conventions

- Code, comments, commit messages, PR descriptions and README in **English**.
- Conventional Commits: `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`, `ci:`, `build:`,
  scoped when it helps (`feat(api): ...`, `feat(web): ...`). One logical change per commit.
- One branch + pull request per roadmap stage; keep the README roadmap up to date.
- **Tests first for domain logic** (chunking, costs, budget, citations, retrieval fusion, eval
  metrics, rate limiting...): describe the expected behaviour to the `test-writer` subagent, review
  the failing tests, commit them (`test(api): specify ...`), then implement until they pass
  (`feat(api): ...`). Glue code (endpoint wiring, config, migrations) gets its tests together with
  the implementation.

## Before finishing a task

1. API: `uv run poe check` (format, lint, pyright, tests)
2. Web: `pnpm format:check && pnpm typecheck && pnpm test && pnpm build`
3. OpenAPI schema and generated client are up to date (see above).
4. **Review before every pull request:** run the `code-reviewer` subagent on the branch's changes.
   When the changes touch LLM calls, prompts, ingestion, admin or auth, also run `security-reviewer`
   (once it exists). Fix the important findings, and list what was reviewed and fixed in the PR
   description.
5. Don't commit, push or open a PR unless asked.
