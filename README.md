# Support Ticket Management System

## Overview

A small internal application for managing support tickets. Users create, update, comment on, search, and progress tickets through a defined lifecycle.

**Scope:** Core requirements only. Stretch/optional features are out of scope.

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Backend | FastAPI | Lean Python API; less bloat than Django for Core CRUD + validation |
| Frontend | Vite + React (JavaScript) | Familiar SPA for three screens; no Next.js/SSR overhead |
| Database | SQLite | Brief allows any RDBMS; simplest local setup and persistence |
| Data access | SQLAlchemy + Alembic | Schema migrations and seed scripts for FastAPI |
| Tests | pytest + FastAPI TestClient | Mandatory state-machine integration tests against the API |
| UI styling | Lightweight CSS (variables/classes) | Linear-inspired look without component-library overhead |

**Acting-as user:** persisted in browser `localStorage` (client-only; no auth).

Stretch remains out of scope (no Docker, auth, OpenAPI, user CRUD).

## Setup

Setup commands will be added when `src/` is scaffolded. Planned layout:

- **Backend:** `src/backend/` — FastAPI app, SQLAlchemy models, Alembic migrations
- **Frontend:** `src/frontend/` — Vite + React SPA
- **Database:** `database/schema-or-migrations/`, `database/seed-data/` — see [database/setup-notes.md](database/setup-notes.md)

Environment variable example: `DATABASE_URL=sqlite:///./tickets.db`

## Running Tests

Test commands will be added when the backend is scaffolded. Mandatory tier: pytest integration tests for ticket status transitions (valid succeed; invalid rejected). See [test-strategy.md](test-strategy.md).
