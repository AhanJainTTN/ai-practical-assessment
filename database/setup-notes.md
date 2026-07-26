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
| `database/seed-data/seed.py` | Wipe-and-reseed script for demo users, tickets, comments |
| `tickets.db` | SQLite database file (gitignored; created in `src/backend/` on migrate/seed) |

Alembic imports SQLAlchemy models from `src/backend/app/*/models.py` via `Base.metadata`.

## Schema

Three tables per [data-model.md](../data-model.md):

| Table | Key columns |
|-------|-------------|
| `users` | `id`, `name`, `email` (unique), `role` (`requester` \| `agent`) |
| `tickets` | `id`, `title`, `description`, `priority`, `status`, `assigned_to` (nullable FK), `created_by` (FK), `created_at`, `updated_at` |
| `comments` | `id`, `ticket_id` (FK), `message`, `created_by` (FK), `created_at` |

Enum-like fields are stored as strings matching the API contract (`Open`, `In Progress`, `Low`, etc.).

Initial migration: `database/schema-or-migrations/versions/c22ab7875b2d_create_users_tickets_comments.py`

## Seed expectations

Minimum seed per requirements (implemented in `seed.py`):

- At least 3 users (mix of `requester` and `agent`)
- At least one ticket per status (`Open`, `In Progress`, `Resolved`, `Closed`, `Cancelled`)
- At least one ticket with comments
- At least 2 tickets created by the same user (for non-trivial CSV export demo)

Current demo seed: 3 users, 6 tickets (all five statuses covered; two `Open`), 2 comments on the first open ticket. Alice (requester) has 3 tickets for CSV export testing.

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

### 3. Run migrations

From `src/backend`:

```bash
uv run alembic -c ../../database/schema-or-migrations/alembic.ini upgrade head
```

Check current revision:

```bash
uv run alembic -c ../../database/schema-or-migrations/alembic.ini current
```

### 4. Seed data

From `src/backend`:

```bash
uv run python ../../database/seed-data/seed.py
```

Wipe-and-reseed: deletes all rows in FK-safe order (comments → tickets → users) then inserts demo data. Safe to re-run before demos.

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
