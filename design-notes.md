# Design Notes

## Architecture Overview (frontend, backend, database)

Three-tier Core architecture:

- **Frontend:** Vite + React (JavaScript) SPA — ticket list, create form, ticket detail; app-wide Acting-as user selector
- **Backend:** FastAPI REST API — validation, state machine enforcement, CSV export
- **Database:** SQLite file via SQLAlchemy; schema managed with Alembic; seed data in `database/seed-data/`

```
Browser (React SPA)  --REST/JSON-->  FastAPI  --SQLAlchemy-->  SQLite (tickets.db)
```

Local dev: frontend and backend run as separate processes (Vite dev server + uvicorn). CORS enabled for local FE origin.

**Why not alternatives (reflection-ready):**
- **Django:** too much framework surface (admin, ORM opinions, project boilerplate) for a small CRUD + state-machine API
- **Next.js / Remix:** SSR/routing/deployment model not needed for three internal screens
- **Postgres:** SQLite satisfies brief (“any RDBMS”) with zero install friction for reviewers
- **shadcn / Tailwind:** aesthetic target is Linear-inspired; achievable with lightweight CSS without extra deps

## Frontend Design

- **Routing:** React Router — `/` (list), `/tickets/new`, `/tickets/:id`
- **State:** React context for Acting-as user (read/write `localStorage`); local component state for forms and API responses
- **API client:** `fetch` to FastAPI base URL (env-configured, e.g. `VITE_API_URL`)
- **Screens:** per [ui-flow.md](ui-flow.md) — list with status filter and CSV export; create form; detail with field edit, status transitions, comments
- **Styling:** CSS variables on Linear dark canvas tokens (`#010102` canvas, surface ladder, lavender `#5e6ad2` accent); compact list rows, hairline borders — no component library
- **Acting-as:** dropdown in app chrome; blocks create, comment, and export when unset; persists in `localStorage`

## Backend Design

- **Structure:** FastAPI app with routers for users, tickets, comments, export
- **Layers:** Pydantic schemas (request/response) → service/domain (state machine, business rules) → SQLAlchemy repositories/models
- **State machine:** centralized transition map; `POST /api/tickets/{id}/transitions` is the only path for status changes; invalid transitions return 400/422
- **Validation:** Pydantic on input; additional checks for FK existence (`createdBy`, `assignedTo`, `ticketId`); `status` on create always forced to `Open` (not client-supplied)
- **CSV export:** `GET /api/tickets/export.csv?createdBy=` — server-side join for assignee/creator names and comment aggregation per [ui-flow.md](ui-flow.md)
- **List:** `GET /api/tickets?status=` — optional filter; default sort `createdAt` descending

See [api-contract.md](api-contract.md) for endpoint outline.

## Database Design

SQLite with three tables aligned to [data-model.md](data-model.md):

- **users** — id, name, email, role (`requester` | `agent`); seeded only
- **tickets** — id, title, description, priority, status, assigned_to (nullable FK), created_by (FK), created_at, updated_at
- **comments** — id, ticket_id (FK), message, created_by (FK), created_at

Migrations in `database/schema-or-migrations/` (Alembic). Seed script in `database/seed-data/` covering minimum demo data from data model.

`DATABASE_URL=sqlite:///./tickets.db` (or relative path under project root).

## Validation Strategy

**Backend (authoritative):**
- Ticket create: non-empty title/description; priority in `Low|Medium|High`; `createdBy` must exist; `status` always `Open`; `assignedTo` optional but must exist if set
- Ticket update: same field rules; `assignedTo` may be null
- Status change: only via transition endpoint; reject invalid transitions
- Comment create: non-empty message; `ticketId` and `createdBy` must exist

**Frontend (UX):**
- Required field hints and disable submit when Acting-as unset
- Status control shows only valid next statuses (backend still enforces)
- Surface FastAPI/Pydantic error `detail` in banners or inline messages

## Error Handling Strategy

- **API:** HTTP 404 for missing resources; 422 for validation; 400 for business-rule failures (e.g. invalid transition)
- **Response shape:** FastAPI default — `{ "detail": "..." }` or field-level validation errors
- **UI:** distinguish validation errors, state-machine errors, missing Acting-as, and network failures with clear copy; no silent failures on create/update/comment/export

## Testing Strategy Link

See [test-strategy.md](test-strategy.md). Mandatory: pytest integration tests via FastAPI TestClient proving all valid transitions succeed and invalid ones are rejected.
