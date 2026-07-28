# Candidate Information

Name: Ahan Jain
Role: Software Engineer
Primary Technology Stack: FastAPI, Vite + React (JavaScript), SQLite
Primary AI Tool Used: Cursor
Project Option Selected: Support Ticket Management System
Assessment Start Date: 2026-07-08
Submission Date:

## Project Summary

Support Ticket Management System — a full-stack mini project for creating, listing, viewing, updating, commenting on, and exporting support tickets with enforced status transitions.

## Tools Used

- Primary AI tool: Cursor
- Backend: FastAPI, SQLAlchemy, Alembic, pytest, uv
- Frontend: Vite, React (JavaScript)
- Database: SQLite
- Styling: lightweight CSS (Linear-inspired dark theme)

## Setup Summary

See [README.md](README.md) for local run instructions:

1. `cd src/backend && uv sync` — migrate (`alembic upgrade head`) and seed
2. `uv run uvicorn main:app --reload` — API on port 8000
3. `cd src/frontend && npm install && npm run dev` — SPA on port 5173

Database workflow: [database/setup-notes.md](database/setup-notes.md). Tests: `cd src/backend && uv run pytest -v`.
