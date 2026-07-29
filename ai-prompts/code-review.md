# Code Review Prompts

## Entry 1 — Pre-submission focused review (2026-07-28)

### Prompt (text or summary)

Focused code review before submission — review only, no refactors. Read requirements, acceptance criteria, api-contract, data-model, backend, frontend, and tests. Priorities: requirements adherence, validation correctness, minimalism (no bloat), consistency, security hygiene. Output summary, findings by severity, and "no action needed" list.

### AI response summary

AI read specs and full codebase. Verdict: Core requirements met — endpoints, shapes, state machine, CSV, Acting-as, validation, and tests align. No blockers or should-fix. Nits: naive UTC timestamps, FE/BE transition map mirror, unnecessary CORS credentials, PATCH silent-ignore of unknown fields. Listed intentionally minimal patterns to avoid over-correcting.

### Accepted

- Review scope and severity grouping (blocker / should-fix / nit)
- "Meets Core / no blockers" conclusion
- Intentionally minimal list (redundant re-queries, 422 on bad status filter, test scope)
- Leaving FE/BE transition map and CORS credentials as low-priority nits

### Changed

- N/A in review pass — follow-up debugging session led to timezone fix (see debugging.md)

### Rejected (and why)

- Stretch features or new dependencies — out of scope per prompt rules
- Broad refactors — review was propose-only; minimal fixes only after judgment
- Adding transition-map API endpoint — would exceed Core minimalism for drift prevention
