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
