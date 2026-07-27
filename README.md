# Support Ticket Management System

## Overview

A small internal application for managing support tickets. Users create, update, comment on, search, and progress tickets through a defined lifecycle.

**Scope:** Core requirements only. Stretch/optional features are out of scope.

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Backend | FastAPI | Lean Python API; less bloat than Django for Core CRUD + validation |
| Frontend | Vite + React (JavaScript) | Familiar SPA for three screens; no Next.js/SSR overhead |
| Database | SQLite | Brief allows any RDBMS; simplest local setup and persistence |
| Data access | SQLAlchemy + Alembic | Schema migrations and seed scripts for FastAPI |
| Python tooling | uv | Fast, reproducible dependency management (`uv.lock`) |
| Tests | pytest + FastAPI TestClient | Mandatory state-machine integration tests against the API |
| UI styling | Lightweight CSS (variables/classes) | Linear-inspired look without component-library overhead |

**Acting-as user:** persisted in browser `localStorage` (client-only; no auth).

Stretch remains out of scope (no Docker, auth, OpenAPI, user CRUD).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Node.js 18+ and npm (frontend)

## Project layout

- **Backend:** `src/backend/` — FastAPI app (feature/hybrid layout: `api/`, `core/`, `users/`, `tickets/`, `comments/`)
- **Frontend:** `src/frontend/` — Vite + React SPA
- **Database:** `database/schema-or-migrations/` (Alembic), `database/seed-data/` — see [database/setup-notes.md](database/setup-notes.md)

## Environment

Copy the example env file and adjust if needed:

```bash
cp .env.example src/backend/.env
cp .env.example src/frontend/.env
```

| Variable | Example | Used by |
|----------|---------|---------|
| `DATABASE_URL` | `sqlite:///./tickets.db` | Backend (relative to `src/backend/` when running uvicorn) |
| `CORS_ORIGINS` | `http://localhost:5173` | Backend |
| `VITE_API_URL` | `http://localhost:8000` | Frontend |

## Backend setup

```bash
cd src/backend
uv sync
```

### Database migrate and seed

Run from `src/backend` (creates `tickets.db` in this directory):

```bash
uv run alembic -c ../../database/schema-or-migrations/alembic.ini upgrade head
uv run python ../../database/seed-data/seed.py
```

The seed script wipes and reseeds demo users, tickets, and comments. Re-run anytime for a predictable demo dataset.

### Start API

```bash
uv run uvicorn main:app --reload
```

API base: `http://localhost:8000` — routes under `/api/*` (see [api-contract.md](api-contract.md)).

## Frontend setup

```bash
cd src/frontend
npm install
npm run dev
```

App: `http://localhost:5173` — ticket list, create form, and detail screens.

## Database migrations

Alembic lives in `database/schema-or-migrations/`. Common commands from `src/backend`:

```bash
uv run alembic -c ../../database/schema-or-migrations/alembic.ini current
uv run alembic -c ../../database/schema-or-migrations/alembic.ini upgrade head
```

See [database/setup-notes.md](database/setup-notes.md) for full database workflow.

## Running tests

From `src/backend`:

```bash
cd src/backend
uv run pytest
```

16 integration tests cover state-machine transitions, validation, and CSV export. See [test-strategy.md](test-strategy.md) and [test-results.md](test-results.md).
