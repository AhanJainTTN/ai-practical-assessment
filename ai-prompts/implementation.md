# Implementation Prompts

## Entry 1 — Backend API milestone (2026-07-26)

### Prompt (text or summary)

Move onto the next step of the implementation plan (after Schema & seed: Backend API — users list, ticket CRUD, transition endpoint, comments, CSV export; validation and state machine in service layer).

### AI response summary

Implemented FastAPI Backend API against `api-contract.md`: Pydantic schemas (camelCase aliases), repositories with eager loading, services with validation + centralized transition map + CSV export, and routers returning real responses.

### Accepted

- Layered users/tickets/comments routers → services → repositories
- State machine enforced only via `POST /api/tickets/{id}/transitions`
- CSV export with agreed columns; header-only when no matching tickets
- 404 / 400 / 422 error mapping per contract

### Changed

- Registered SQLAlchemy models in `main.py` so relationships resolve at runtime
- README note updated (no longer “stub routes”)

### Rejected (and why)

- No new dependencies (used stdlib `csv` for export)
- Frontend UI deferred to next milestone

## Entry 2 — Frontend UI milestone (2026-07-27)

### Prompt (text or summary)

Implement Frontend UI milestone: Acting-as selector populated from users API, ticket list with status filter and CSV export, create form, detail with edit/transitions/comments, Linear-inspired CSS.

### AI response summary

Built three real React screens wired to existing `apiClient`: list with filter/export, create with Acting-as gate, detail with field edit, valid transition buttons, and comments. Added shared constants (transition map), error formatting, CSV blob download, and extended CSS.

### Accepted

- Acting-as dropdown loads seeded users and persists in `localStorage`
- List filter, create link, CSV export gated on Acting-as
- Create/detail forms use camelCase API payloads
- Frontend transition map mirrors backend; backend remains authoritative
- Error banners for API/validation failures

### Changed

- Replaced `Placeholders.jsx` with `TicketListPage`, `CreateTicketPage`, `TicketDetailPage`
- Hardened `api/client.js` for FastAPI error shapes and CSV blob export
- README updated (no longer “placeholder routes”)

### Rejected (and why)

- No new npm dependencies
- State-machine pytest suite deferred to next milestone
