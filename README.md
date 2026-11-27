# Ask my portfolio

An AI assistant that answers questions about my work. Ask it what I have built, which technologies I
have used or how a project works, and it answers **only from my CV, READMEs and source code**, citing
every claim with a link to the document or the exact lines of code on GitHub.

> 🚧 Work in progress. The project is being built in stages, one pull request per stage; see the roadmap.

## How it works

Retrieval-augmented generation (RAG):

1. **Indexing:** my CV, project READMEs and code are split into chunks (markdown by headings, code by
   functions and classes), turned into embeddings and stored in PostgreSQL with pgvector.
2. **Answering:** a question is embedded, the most relevant chunks are retrieved, and Claude answers
   from them with citations. The answer is streamed to the browser.
3. **Measuring:** an evaluation set of questions checks retrieval and answer quality, so every change
   (model, search, prompt) is compared with numbers, not impressions.

## Tech stack

| Layer      | Technology                                                                 |
| ---------- | -------------------------------------------------------------------------- |
| API        | Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2 (async), Alembic            |
| Data       | PostgreSQL 17 + pgvector                                                    |
| LLM        | Claude (Anthropic SDK), Haiku by default, model switchable at runtime _(planned)_ |
| Web        | Next.js 16, React 19, TanStack Query, client generated from OpenAPI (orval) |
| Quality    | ruff, pyright (strict), pytest + testcontainers, Vitest, GitHub Actions     |

## Getting started

Requirements: [uv](https://docs.astral.sh/uv/), Node.js 24 with pnpm (via Corepack), Docker.

Once, after cloning:

```bash
cp .env.example .env
cp -r content.example content   # sample content; replace it with your own CV (see below)
cd web && pnpm install
```

Then, in two terminals:

```bash
cd api && uv run poe dev    # PostgreSQL + pgvector (Docker), migrations, API on http://localhost:8000
cd web && pnpm dev          # web on http://localhost:3001
```

`uv run` installs Python 3.13 and the dependencies on first use. API docs: http://localhost:8000/api/docs.
Other API tasks (`check`, `test`, `format`, `openapi`, ...): `cd api && uv run poe`.

## Your own content

The assistant answers from the markdown files in `content/`. That folder is **git-ignored**: the
code is public, but my real CV and about-me are deployed to the server only, so they can't be bulk
downloaded from the repository and can be changed without leaving a trace in git history.

`content.example/` holds fictional sample content (Jane Doe) used by tests and CI. To run the
assistant about yourself, put your own `cv.md` and `about.md` in `content/` (the sample folder's
README explains how to structure them).

## Project structure

```
api/                 FastAPI modular monolith (app/modules/<feature>/), Alembic migrations, tests
  openapi.json       API contract, exported from FastAPI and committed
web/                 Next.js app
  src/lib/api/generated/   typed client + TanStack Query hooks generated from openapi.json
content/             real content (private, git-ignored)
content.example/     public sample content for tests and local runs
docker-compose.yml   local PostgreSQL + pgvector
```

## Roadmap

- [x] Setup: FastAPI, Next.js, PostgreSQL + pgvector, OpenAPI client generation, CI
- [ ] Indexing: CV and about-me markdown, local multilingual embeddings
- [ ] Vector search
- [ ] Answers with citations, model registry, cost tracking, daily budget
- [ ] Streaming chat UI with feedback
- [ ] Admin panel: conversations, traces, costs, runtime settings (GitHub OAuth)
- [ ] Indexing GitHub repositories, code chunked by functions with permalinks to lines
- [ ] Evaluation set: retrieval and answer quality, model comparison
- [ ] Hybrid search (full-text + vectors, reciprocal rank fusion)
- [ ] Abuse protection: rate limiting, Turnstile, answer cache, budget alerts
- [ ] Follow-up questions (multi-turn)
- [ ] Automatic re-indexing on push (GitHub webhooks, Postgres job queue)
- [ ] Live demo
