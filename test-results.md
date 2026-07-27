# Test Results

## Summary

**16 passed, 0 failed** — run on 2026-07-27 from `src/backend` with `uv run pytest -v`.

## Runs

| Command | Result | Notes |
|---------|--------|-------|
| `cd src/backend && uv run pytest -v` | 16 passed | ~0.22s |

## Coverage

### State machine (mandatory)

- Valid transitions: Open → In Progress, In Progress → Resolved, Resolved → Closed, Open → Cancelled, In Progress → Cancelled
- Invalid transitions: Open → Closed, Resolved → In Progress, Closed → Open, Cancelled → Open
- Missing ticket transition → 404

### API validation (recommended)

- Create with empty title → 422
- Invalid priority → 422
- Assign to non-existent user → 422
- Comment on missing ticket → 404
- List filter by status returns correct subset
- CSV export with no matching tickets returns headers only (200)
