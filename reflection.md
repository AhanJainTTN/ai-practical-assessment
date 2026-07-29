# Reflection

## What I Built

A Core Support Ticket Management System: FastAPI backend (hybrid router/service/repository layout), Vite + React SPA, SQLite with Alembic migrations and seed data. Features include Acting-as user selection, ticket CRUD, status filter, enforced state machine, comments, CSV export, and 16 pytest integration tests. UI uses a Linear-inspired dark theme with hand-rolled CSS (no component library).

Stretch is excluded: no auth, Docker, OpenAPI, or user admin UI.

## How I Used AI (across the lifecycle)

Cursor across separate chats mapped to `ai-prompts/`:

1. **Planning** — repo scaffold from PDF templates; requirements lock; phase sequencing (requirements before stack)
2. **Design** — stack criteria; FastAPI + Vite/React (JS) + SQLite; Linear aesthetic without shadcn
3. **Implementation** — scaffold (uv, Alembic under `database/`), schema/seed, API, frontend UI
4. **Testing** — state-machine and validation suite
5. **Code review + debugging** — pre-submission review; timezone fix via shared `UtcDateTime`

Workflow: Plan mode for scoped plans in `plans/` → Agent "implement the plan" → Ask for commits and judgment calls.

## What AI Helped With Most

- Bootstrapping the PDF-required doc tree and folder layout quickly
- Generating consistent API layers (schemas, repositories, services, routers) from `api-contract.md`
- pytest harness with in-memory SQLite and parametrized transition tests
- Linear dark reskin from a design reference without adding dependencies
- Structured code review with severity grouping and an "don't over-correct" list

## What AI Got Wrong

- **Timestamp serializers during API implementation** — AI added `to_iso_z()` and field serializers to match contract `Z` examples; I rejected that as unnecessary overhead and updated the contract to match default ISO output instead
- **Over-eager fixes** — review initially suggested optional serializer work; I asked for impact analysis before changing anything
- AI can propose Stretch-shaped patterns (OpenAPI clients, transition-map endpoints) — I filtered those out explicitly

## How I Validated AI Output

- Contract audit against `api-contract.md` after backend API milestone
- `uv run pytest -v` after each major backend change (16 tests)
- Smoke tests against migrated + seeded database
- Manual UI flows (Acting-as, filter, create, transition, comment, CSV)
- Final focused code review against acceptance criteria before submission

## What I Would Improve Next

- Pagination on ticket list (unbounded `GET /api/tickets` is the real scale concern, not UTC serialization)
- Auth and server-side identity (Stretch)
- Single source of truth for transition map (or a test that FE/BE maps stay in sync)
- E2E browser tests for UI regressions

## Reusable Workflow (prompts, rules, specs, templates)

- **Requirements before stack** — product clarifications shape API more than framework choice
- **Plan → Agent** with locked decisions in `plans/`; don't edit plan files during implement
- **PDF-shaped prompt history** in `ai-prompts/` (prompt, summary, accepted, changed, rejected)
- **Scoped review prompts** — requirements first, minimalism explicit, propose-only then fix
- **Separate chats per phase** for clean exports and lifecycle evidence
- Archive init plan under `tool-specific/cursor-workflow/`
