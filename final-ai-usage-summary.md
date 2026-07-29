# Final AI Usage Summary

## Across the Lifecycle

| Phase | Tool | Outcome |
|-------|------|---------|
| Repo init | Cursor Plan + Agent | PDF-aligned docs, `ai-prompts/` structure, Core brief seeded |
| Requirements | Cursor Plan + Agent | Acting-as, priority, filter, CSV, roles locked |
| Design / stack | Cursor Ask + Plan | FastAPI, Vite/React (JS), SQLite; no shadcn |
| Implementation | Cursor Plan + Agent | Scaffold → schema/seed → API → UI (milestones in `plans/`) |
| Testing | Cursor Agent | 16 pytest integration tests |
| Review / debug | Cursor Ask + Agent | Pre-submission review; `UtcDateTime` fix |

Primary pattern: **context-rich prompts → plan → implement → validate → record in `ai-prompts/`**.

## Key Prompts

1. **Repo init from PDF** — [`ai-prompts/planning.md`](ai-prompts/planning.md) Entry 1 — scope Stretch out, submission templates
2. **Lock Core requirements (no stack)** — planning Entry 4 — product defaults across four docs
3. **Stack + design** — [`ai-prompts/design.md`](ai-prompts/design.md) — FastAPI/React/JS/SQLite, Linear without shadcn
4. **Implement milestones** — [`ai-prompts/implementation.md`](ai-prompts/implementation.md) — scaffold choices, API, contract audit
5. **Pre-submission review** — [`ai-prompts/code-review.md`](ai-prompts/code-review.md) — requirements adherence, minimalism
6. **Timezone fix** — [`ai-prompts/debugging.md`](ai-prompts/debugging.md) — shared `UtcDateTime` after impact analysis

## Judgments and Corrections

- **Stretch permanently out of scope** — rejected Docker, auth, OpenAPI, shadcn, RBAC in every phase
- **Requirements before stack** — rejected stack-first ordering
- **JS over TS, lightweight CSS over shadcn** — familiarity and minimal deps
- **Rejected `Z` serializers on first API pass** — updated contract instead of serializer overhead; later added `UtcDateTime` for a real display bug found in review
- **Rejected review over-correction** — kept FE/BE transition mirror, CORS credentials, redundant re-queries as intentional minimal patterns
- **Scaffold choices** — Full milestone, Alembic under `database/`, flat domains, uv

Full prompt history: [`ai-prompts/`](ai-prompts/). Workflow detail: [`tool-workflow.md`](tool-workflow.md).
