# Testing Prompts

## Entry 1 — State-machine integration tests (2026-07-27)

### Prompt (text or summary)

Finish remaining implementation plan steps: add mandatory pytest state-machine integration tests (plus recommended API validation cases), run them, and polish assessment docs (`test-results.md`, `acceptance-criteria.md`, `pr-description.md`).

### AI response summary

Added `tests/conftest.py` with isolated in-memory SQLite (`StaticPool`), `get_db` override, and user seed fixture. Created `tests/helpers.py` for ticket creation/transition helpers. Wrote `tests/test_state_machine.py` (9 cases: 5 valid transitions, 4 invalid, 1 missing-ticket 404) and `tests/test_api_validation.py` (6 cases: validation, FK checks, list filter, CSV headers-only). All 16 tests pass.

### Accepted

- In-memory SQLite with `StaticPool` for test isolation
- Parametrized valid/invalid transition tests against live API
- Thin validation/export tests backing acceptance criteria
- `test-results.md`, `acceptance-criteria.md`, `pr-description.md` filled in

### Changed

- README test section updated (removed "after tests are added" wording)

### Rejected (and why)

- No frontend component tests — not required for Core per `test-strategy.md`
- No separate unit tests for `ALLOWED_TRANSITIONS` — integration tier is mandatory and sufficient
