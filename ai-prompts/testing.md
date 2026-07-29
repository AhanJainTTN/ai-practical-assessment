# Testing Prompts

## Entry 1 — State-machine integration tests (2026-07-27)

### Prompt (text or summary)

Finish with the remaining implementation plan steps.

### AI response summary

AI identified milestones 5–6 as remaining: pytest state-machine integration suite plus docs polish. Implemented isolated in-memory SQLite test harness (`StaticPool`, `get_db` override, user seed fixture), helpers for ticket creation/transitions, `test_state_machine.py` (9 cases: 5 valid transitions, 4 invalid, 1 missing-ticket 404), and `test_api_validation.py` (6 validation/export cases). All 16 tests pass via `uv run pytest -v`. Also updated test-results.md, acceptance-criteria.md, pr-description.md, and README test section.

### Accepted

- In-memory SQLite with `StaticPool` for test isolation
- Parametrized valid/invalid transition tests against live API via TestClient
- Thin validation/export tests backing acceptance criteria
- Helpers in `tests/helpers.py` (not imported from `conftest.py` per pytest convention)
- test-results.md filled with run summary; acceptance-criteria.md checked off

### Changed

- Moved ticket/transition helpers out of `conftest.py` into `tests/helpers.py` during implementation

### Rejected (and why)

- Frontend component tests — not required for Core per test-strategy.md
- Separate unit tests for `ALLOWED_TRANSITIONS` map — integration tier is mandatory and sufficient for this assessment
