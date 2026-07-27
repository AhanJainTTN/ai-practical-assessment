# Implementation Prompts

## Entry 1 — Scaffold layout (2026-07-26)

### Prompt (text or summary)

Begin implementation with project scaffolding. FastAPI backend: feature/hybrid layout — thin `main` → aggregate `api` → per-domain router / service / repository / schemas. Follow-up choices: **Full + A** (full milestone including frontend; Alembic under `database/schema-or-migrations/`). Flatten domain folders (no `domains/` wrapper). Use **uv** for Python.

### AI response summary

AI asked two clarifying questions (scaffold scope, Alembic location), then implemented the full Scaffold milestone: hybrid FastAPI backend with flat `users/`, `tickets/`, `comments/` domains; Alembic config under `database/schema-or-migrations/`; Vite + React frontend with placeholder routes and Acting-as context; `.env.example`; README and setup-notes updates. Stub routes aligned with api-contract.

### Accepted

- **Full milestone** — backend + frontend + env + README in one pass
- **Alembic option A** — versions under `database/`, models/session in `src/backend/`
- **Flat domain folders** — `app/users/`, `app/tickets/`, `app/comments/` alongside `app/api/` and `app/core/`
- **uv** — `pyproject.toml` + `uv.lock`; `uv sync` / `uv run` for all Python commands

### Changed

- Plan updated from nested `domains/` to flat per-feature folders after my question

### Rejected (and why)

- **`domains/` wrapper folder** — unnecessary nesting for Core; hybrid split is router/service/repository/schemas, not an extra directory level
- **Backend-only scaffold** — chose full milestone to get runnable FE/BE locally
- **Alembic option B** (full tree under `src/backend/`) — assessment folder structure expects migrations under `database/`

---

## Entry 2 — Schema and seed (2026-07-26)

### Prompt (text or summary)

Move on to the next milestone (Schema & seed).

### AI response summary

AI implemented SQLAlchemy models for User, Ticket, and Comment per data-model.md; initial Alembic migration; wipe-and-reseed script with demo data (3 users, 6 tickets covering all statuses, 2 comments). Moved `utcnow` to `app/core/time.py` to avoid circular imports.

### Accepted

- String enums, snake_case columns, relationships per data-model
- Wipe-and-reseed seed script for predictable demos
- Demo data: Alice has 3 tickets for CSV export testing

### Changed

- `utcnow` extracted to shared `core/time` module during implementation

### Rejected (and why)

- N/A

---

## Entry 3 — Backend API (2026-07-26)

### Prompt (text or summary)

Move onto the next step of the implementation plan.

### AI response summary

AI identified Backend API as the next milestone and implemented the full API per api-contract.md: Pydantic schemas (camelCase aliases), repositories with eager loading, services with validation and centralized transition map, CSV export, and wired routers. Smoke-tested against migrated + seeded DB.

### Accepted

- All Core endpoints: users list, ticket CRUD, transitions, comments, CSV export
- State machine enforced only via `POST /api/tickets/{id}/transitions`
- Validation and error mapping: 400 / 404 / 422 per contract
- Model registration in `main.py` for relationship resolution

### Changed

- N/A

### Rejected (and why)

- New dependencies for CSV — used stdlib `csv` module

---

## Entry 4 — Contract audit and timestamps (2026-07-26)

### Prompt (text or summary)

Did you stick to `@api-contract.md`?

### AI response summary

AI audited live responses against the contract. Found endpoints, shapes, aliases, status rules, error codes, and CSV columns conformed. One deviation: timestamps — contract showed `Z` suffix; API returned naive ISO without `Z`. AI added `to_iso_z()` helper and field serializers to fix it. I then rejected that fix and asked to update the contract instead.

### Accepted

- AI's honest contract audit (verified shapes, error codes, CSV columns)
- Plain Pydantic default datetime serialization (no `Z` suffix)
- api-contract.md examples updated to match actual API output
- Stricter `422` on invalid status filter (contract silent on bad filter values)

### Changed

- Reverted AI's timestamp serializer fix after review
- Updated api-contract.md timestamp examples to drop `Z` suffix

### Rejected (and why)

- **`to_iso_z()` serializers and field_serializer overhead** — unnecessary complexity for SQLite naive datetimes; contract updated to match reality instead of forcing `Z` formatting

---

## Entry 5 — Frontend UI (2026-07-27)

### Prompt (text or summary)

Start the next milestone (Frontend UI).

### AI response summary

AI implemented three real React screens wired to the API: list with status filter and CSV export, create with Acting-as gate, detail with field edit, valid transition buttons, and comments. Added shared constants (transition map mirroring backend), error formatting, CSV blob download, ErrorBanner, and Linear-inspired CSS. Production build passes.

### Accepted

- Acting-as dropdown from `GET /api/users`, persisted in `localStorage`
- Frontend transition map mirrors backend; backend remains authoritative
- List filter, create link, CSV export gated on Acting-as
- camelCase API payloads; error banners for API/validation failures
- Replaced placeholder pages with TicketListPage, CreateTicketPage, TicketDetailPage

### Changed

- N/A

### Rejected (and why)

- New npm dependencies — kept vanilla React + hand-rolled CSS
- State-machine pytest suite — deferred to next milestone per implementation plan
