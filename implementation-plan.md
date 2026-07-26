# Implementation Plan

## Overview

Build the Core Support Ticket Management System with a locked stack:

- **Frontend:** Vite + React (JavaScript) SPA
- **Backend:** FastAPI + SQLAlchemy + Alembic
- **Database:** SQLite
- **Tests:** pytest + FastAPI TestClient (mandatory state-machine integration tests)

**Stretch/optional work is deliberately excluded from scope** — no auth, Docker, OpenAPI, user CRUD, or richer data model.

## Milestones

1. **Scaffold** — `src/backend/` (FastAPI, deps, Alembic init), `src/frontend/` (Vite + React), `.env.example`, update README setup commands
2. **Schema & seed** — Alembic migration for users/tickets/comments; seed script meeting minimum demo data
3. **Backend API** — users list, ticket CRUD, transition endpoint, comments, CSV export; validation and state machine in service layer
4. **Frontend UI** — Acting-as selector (`localStorage`), list + filter + export, create form, detail with edit/transitions/comments; Linear-inspired CSS
5. **State-machine tests** — pytest integration tests for all valid transitions and representative invalid ones
6. **Docs polish** — `api-contract.md` finalized, `test-results.md`, acceptance criteria checked, `pr-description.md` draft

## Task Breakdown

Detailed per-endpoint tasks will be tracked during implementation. High-level order:

| Phase | Work |
|-------|------|
| Backend foundation | Models, schemas, DB session, Alembic, seed |
| Ticket API | List (status filter), create, get, patch fields, transitions |
| Comment API | List on detail, create comment |
| Export | CSV endpoint with joined columns |
| Frontend shell | Router, API client, Acting-as context, layout/chrome |
| Frontend screens | List, create, detail |
| Tests | State-machine integration suite |
| README | End-to-end local run instructions |

## AI Usage Plan

- **Planning / stack:** Cursor for requirement and stack decisions; capture prompts in `ai-prompts/`
- **Implementation:** Generate scaffolding and boilerplate with Cursor; review and adjust validation/state-machine logic manually
- **Testing:** Use AI to draft pytest cases; verify against real API responses
- **Debugging:** Paste tracebacks and failing tests; iterate with targeted fixes
- **Review:** Self-review via Cursor before marking acceptance criteria complete
- **Documentation:** AI-assisted drafts for API contract and PR description; human edit for accuracy

## Risks

| Risk | Impact |
|------|--------|
| CORS misconfiguration | Frontend cannot reach API in local dev |
| SQLite file path confusion | Migrations/seed write to wrong location; app sees empty DB |
| State machine logic duplicated in FE and BE | UI and API disagree on valid transitions |
| Acting-as not gated in UI | Create/comment/export without user context |
| Over-scoping UI polish | Time lost on design system vs Core features |

## Mitigation

- Configure FastAPI CORS for Vite dev origin early; smoke-test `fetch` from FE
- Document single `DATABASE_URL` and run all DB commands from consistent working directory
- Single transition map in backend service; FE derives allowed next statuses from same rules (or from API)
- Block mutating actions and export when Acting-as is null; show clear prompt
- CSS variables + three screens only; defer non-Core polish
