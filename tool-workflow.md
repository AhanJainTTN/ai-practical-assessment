# AI Tool Workflow

## Primary AI tool used

**Cursor** — Plan mode for scoped milestones and artifact updates; Agent mode for implementation; Ask mode for commit messages, sequencing judgment, and follow-up questions (e.g. timezone impact).

## How you provide project context to the tool

- Attach or `@` the assessment PDF and seeded docs (`requirements-analysis.md`, `acceptance-criteria.md`, `data-model.md`, `ui-flow.md`, `api-contract.md`, `implementation-plan.md`)
- `@` source trees (`src/backend/`, `src/frontend/src/`, `tests/`) when implementing or reviewing
- **Separate chats per lifecycle phase** (repo init → requirements → stack → scaffold → API → UI → tests → review) so exports map cleanly to `ai-prompts/`
- **Plan files** under `plans/` capture locked decisions before Agent runs ("Implement the plan as specified; do not edit the plan file")
- Archive completed plans under `tool-specific/cursor-workflow/` (e.g. repo-init scaffold)

## How you use AI for requirement analysis

1. New chat with explicit rules: Core only, Stretch out of scope, **no stack yet**
2. AI reads clarifications/assumptions in `requirements-analysis.md` and proposes concrete defaults
3. Plan: [`lock_core_requirements_f3e66fd8.plan.md`](plans/lock_core_requirements_f3e66fd8.plan.md) → Agent updates four docs
4. Locked: Acting-as, priority enum, status filter, CSV rules, display-only roles

## How you use AI for planning and design

- **Repo init:** [`repo_init_scaffold_a94309dc.plan.md`](plans/repo_init_scaffold_a94309dc.plan.md) — PDF submission templates, empty placeholders
- **Stack lock:** [`lock_stack_artifacts_f9f62696.plan.md`](plans/lock_stack_artifacts_f9f62696.plan.md) — FastAPI + Vite/React (JS) + SQLite, rationale across artifacts
- **UI:** [`linear_ui_redesign_2f13717c.plan.md`](plans/linear_ui_redesign_2f13717c.plan.md) — dark Linear tokens, no new deps
- Requirements before stack (human + AI judgment) to avoid reverse-fitting product to framework

## How you use AI for code generation

Pattern: **Plan → clarifying questions → lock choices → Agent implement**

| Milestone | Plan | Key human choices |
|-----------|------|-------------------|
| Scaffold | `project_scaffold_setup_ff37af47` | Full + A (Alembic under `database/`), flat domains, **uv** |
| Schema & seed | `schema_and_seed_95d1fa13` | Models per data-model, wipe-and-reseed |
| Backend API | (inline in chat 5) | Contract-driven layers |
| Frontend UI | `frontend_ui_milestone_3c33b0b1` | Three screens, no new npm deps |
| Tests + docs | `finish_remaining_milestones_df2ca9e2` | pytest TestClient, 16 cases |

Hybrid FastAPI layout: `main` → `api` router → per-domain `router` / `service` / `repository` / `schemas`.

## How you validate AI-generated code

- Smoke-test API against migrated + seeded DB after backend milestone
- **Contract audit:** "Did you stick to api-contract.md?" — caught timestamp shape drift; rejected serializer bloat, updated contract instead (later fixed display via `UtcDateTime` after review)
- `uv run pytest -v` — 16 integration tests (state machine + validation + CSV)
- Manual UI: Acting-as → list/filter → create → detail → transition → comment → export CSV
- Pre-submission **focused code review** (chat 9) against acceptance criteria before final fix

## How you use AI for testing

- Plan: `finish_remaining_milestones_df2ca9e2` — in-memory SQLite (`StaticPool`), `get_db` override, helpers in `tests/helpers.py`
- Parametrized valid/invalid transitions; validation and header-only CSV cases
- Re-run full suite after review fixes (timezone)

## How you use AI for debugging

- Code review surfaced timezone nit → follow-up chat for impact, fix options, performance, shared-type pattern
- Implemented `UtcDateTime` only after understanding display-only scope and rejecting duplicated `as_utc` calls
- Documented in `debugging-notes.md` and `review-fixes.md`

## How you use AI for code review

- Structured prompt: requirements adherence first, then correctness, minimalism, consistency, security
- Rules: no Stretch, smallest fix per finding, propose-only first pass
- Accepted "meets Core / no blockers"; implemented one nit (UTC serialization); rejected over-correction of intentional minimal patterns

## What information you avoid sharing unnecessarily with AI tools

- Secrets, API keys, `.env` contents (use `.env.example` only)
- Assessment PDF kept local and untracked in git when following init plan
- No production credentials or unrelated personal data in prompts

## How you would reuse this workflow in a real project

1. **Requirements and acceptance criteria before stack and codegen**
2. **Plan-mode milestones** with explicit out-of-scope boundaries
3. **Separate chats** per phase for auditable prompt history (`ai-prompts/` PDF entry shape)
4. **Human judgment on AI output** — reject bloat (Django, shadcn, premature serializers), accept only what fits scope
5. **Validate with contract checks, integration tests, and a final review pass** before ship
6. Archive plans and export selected chats as lifecycle evidence
