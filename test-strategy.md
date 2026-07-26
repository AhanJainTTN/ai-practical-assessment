# Test Strategy

## Test Scope

Core functionality for the Support Ticket Management System. Stretch/optional features are out of scope.

Mandatory: integration tests must prove state-machine rules (valid transitions succeed; invalid transitions are rejected).

## Unit Tests

Optional for Core. Business logic (state machine) may be tested in isolation if extracted to a pure function, but the mandatory tier is API integration.

## Component Tests

Not required for Core mandatory tier. Frontend behavior validated manually against acceptance criteria.

## API / Integration Tests

**Framework:** pytest + FastAPI `TestClient` against the real app with a test SQLite database (in-memory or temp file).

**Setup:** Apply migrations (or create schema); seed minimal users and at least one ticket per status where needed.

**Mandatory — state machine:**
- Valid transitions succeed:
  - Open → In Progress
  - In Progress → Resolved
  - Resolved → Closed
  - Open → Cancelled
  - In Progress → Cancelled
- Invalid transitions are rejected (e.g. Open → Closed, Resolved → In Progress, Closed → any)

**Additional integration tests (recommended):**
- Create ticket with missing required fields → 422
- Invalid priority → rejected
- Transition on non-existent ticket → 404
- Comment on non-existent ticket → 404
- Assign to non-existent user → rejected
- List filter by status returns correct subset
- CSV export with `createdBy` filter; header-only when no matches

## Edge Case Tests

Covered in integration suite where practical:

- Invalid status transitions (primary mandatory focus)
- Empty required fields on create/update
- Invalid priority values
- Non-existent ticket/user FK references
- CSV export with zero matching tickets (headers only, 200)

## Tests Not Covered (and why)

- **Frontend unit/component tests:** not mandatory for Core; manual UI verification sufficient for scope
- **E2E browser tests (Playwright/Cypress):** out of scope unless time permits; API integration tests cover backend rules
- **Load/performance tests:** not required for assessment scale
- **Auth/RBAC tests:** Stretch auth excluded; roles are display-only
