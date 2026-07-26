# Database Setup Notes

## Database choice

**SQLite** — satisfies the assessment brief (“use any RDBMS”) with the simplest local setup: single file, no server install, easy reset for demos and tests.

Connection string example:

```
DATABASE_URL=sqlite:///./tickets.db
```

## Layout

| Path | Purpose |
|------|---------|
| `database/schema-or-migrations/` | Alembic config (`alembic.ini`, `env.py`, `versions/`) |
| `database/seed-data/` | Seed script for users, tickets, comments (next milestone) |
| `tickets.db` | SQLite database file (gitignored; created on migrate/seed in `src/backend/`) |

Alembic imports SQLAlchemy `Base` from `src/backend/app/core/database.py`. Models and the first migration revision are added in the Schema & seed milestone.

## Schema

Three tables per [data-model.md](../data-model.md): `users`, `tickets`, `comments`. Foreign keys for `created_by`, `assigned_to`, `ticket_id`. Enum-like columns for `priority`, `status`, and `role`.

## Seed expectations

Minimum seed per requirements:

- At least 3 users (mix of `requester` and `agent`)
- At least one ticket per status (`Open`, `In Progress`, `Resolved`, `Closed`, `Cancelled`)
- At least one ticket with comments
- At least 2 tickets created by the same user (for non-trivial CSV export demo)

## Local setup

### 1. Install backend dependencies

```bash
cd src/backend
uv sync
```

### 2. Configure environment

```bash
cp ../../.env.example .env
```

`DATABASE_URL` is relative to the backend working directory (`src/backend/`).

### 3. Run migrations (when available)

From `src/backend`:

```bash
uv run alembic -c ../../database/schema-or-migrations/alembic.ini upgrade head
```

Scaffold state: Alembic is initialized; `versions/` is empty until the first migration is added.

Check current revision:

```bash
uv run alembic -c ../../database/schema-or-migrations/alembic.ini current
```

### 4. Seed data (when available)

Seed script path: `database/seed-data/` — commands documented in the Schema & seed milestone.

### 5. Start the API

```bash
uv run uvicorn main:app --reload
```

## Environment variables

| Variable | Example | Notes |
|----------|---------|-------|
| `DATABASE_URL` | `sqlite:///./tickets.db` | SQLite file path relative to `src/backend/` |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated origins for Vite dev server |

No secrets required for Core (no auth).
