# Database Setup Notes

## Database choice

**SQLite** — satisfies the assessment brief (“use any RDBMS”) with the simplest local setup: single file, no server install, easy reset for demos and tests.

Connection string example:

```
DATABASE_URL=sqlite:///./tickets.db
```

## Planned layout

| Path | Purpose |
|------|---------|
| `database/schema-or-migrations/` | Alembic migration scripts (created when backend is scaffolded) |
| `database/seed-data/` | Seed SQL or Python seed script for users, tickets, comments |
| `tickets.db` | SQLite database file (gitignored; created on migrate/seed) |

## Schema

Three tables per [data-model.md](../data-model.md): `users`, `tickets`, `comments`. Foreign keys for `created_by`, `assigned_to`, `ticket_id`. Enum-like columns for `priority`, `status`, and `role`.

## Seed expectations

Minimum seed per requirements:

- At least 3 users (mix of `requester` and `agent`)
- At least one ticket per status (`Open`, `In Progress`, `Resolved`, `Closed`, `Cancelled`)
- At least one ticket with comments
- At least 2 tickets created by the same user (for non-trivial CSV export demo)

## Local setup (commands TBD)

Concrete migrate and seed commands will be documented here and in [README.md](../README.md) when the FastAPI backend is scaffolded. Expected flow:

1. Create virtualenv and install backend dependencies
2. Run Alembic migrations to create schema
3. Run seed script to populate demo data
4. Start FastAPI — app reads `DATABASE_URL` from environment or `.env` (not committed)

## Environment variables

| Variable | Example | Notes |
|----------|---------|-------|
| `DATABASE_URL` | `sqlite:///./tickets.db` | SQLite file path relative to backend working directory |

No secrets required for Core (no auth).
