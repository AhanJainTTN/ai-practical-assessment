# PR Description

## Summary

Implements the Core Support Ticket Management System — a full-stack app for creating, listing, viewing, updating, commenting on, and exporting support tickets with enforced status transitions.

## Features Implemented

- Acting-as user selector (persisted in `localStorage`) gating create, comment, and export
- Ticket list with status filter and CSV export
- Create ticket form (title, description, priority, optional assignee)
- Ticket detail with field editing, status transitions, and comments
- Backend state machine enforced via dedicated transition endpoint
- Seed data covering all ticket statuses and demo scenarios

## Technical Changes

- **Backend:** FastAPI with layered routers → services → repositories; Pydantic validation; centralized `ALLOWED_TRANSITIONS` map
- **Frontend:** Vite + React SPA with React Router; `fetch` API client; Linear-inspired CSS
- **Tests:** pytest + FastAPI TestClient integration suite (16 tests) with isolated in-memory SQLite

## Database Changes

- Alembic migration for `users`, `tickets`, `comments` tables
- Seed script with 3 users, 6 tickets (all statuses), and sample comments

## Testing Done

```bash
cd src/backend && uv run pytest -v
# 16 passed
```

Covers all mandatory state-machine transitions (valid + invalid), plus validation and CSV export edge cases. See [test-results.md](test-results.md).

## AI Usage Summary

Cursor used for scaffolding, API/frontend implementation, test drafting, and documentation. Prompt history in `ai-prompts/`.

## Screenshots / Demo Notes

1. Start backend (`uvicorn`) and frontend (`npm run dev`)
2. Select Acting-as user in header
3. Browse tickets, filter by status, export CSV
4. Create a ticket, open detail, transition status, add comments

## Known Limitations

- Core scope only — no auth, Docker, OpenAPI docs, or user CRUD
- Acting-as is client-side only (no server-side identity)
- Frontend validated manually; no component tests

## Future Improvements

- Auth and role-based permissions
- Pagination on ticket list
- Real-time updates / websockets
- E2E browser tests (Playwright)
