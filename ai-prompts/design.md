# Design Prompts

## Entry 1 — Tech stack lock and design-notes

### Prompt (text or summary)

Stack finalized: FastAPI backend, Vite + React (JavaScript) frontend, SQLite database. Linear-inspired UI aesthetic without shadcn/Tailwind. Update design-notes and related artifacts with architecture rationale.

### AI response summary

Filled [design-notes.md](../design-notes.md) with three-tier architecture (React SPA → FastAPI → SQLite), frontend routing/state/styling approach, backend layers and state machine design, validation and error handling strategy. Documented why not Django, Next.js, Postgres, or shadcn. Linked to data-model, api-contract, and test-strategy.

### Accepted

- FastAPI + Vite/React (JS) + SQLite as locked stack
- SQLAlchemy + Alembic for schema/seed
- Acting-as user in `localStorage`
- Lightweight CSS for Linear-inspired look
- Centralized backend state machine; CSV export server-side

### Changed

N/A — initial design documentation from locked stack.

### Rejected (and why)

- Django — too much boilerplate for Core scope
- Next.js — unnecessary SSR/routing complexity
- Postgres — SQLite sufficient per brief; simpler reviewer setup
- shadcn/Tailwind — aesthetic achievable without extra deps
