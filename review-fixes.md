# Review Fixes

## Fix 1 — UTC-aware timestamp serialization

### Finding

Code review flagged naive datetimes from SQLite: API and CSV emitted strings like `2026-07-27T16:00:00` without a timezone. `formatDateTime` in the frontend uses `new Date(value)`, which treats offset-less strings as **local** time, skewing displayed clocks by the client's UTC offset (e.g. ~5.5h in IST).

### Change

- Added `ensure_utc()` in [`src/backend/app/core/time.py`](src/backend/app/core/time.py)
- Added `UtcDateTime = Annotated[datetime, AfterValidator(ensure_utc)]` in [`src/backend/app/core/types.py`](src/backend/app/core/types.py)
- Wired `UtcDateTime` on response `created_at` / `updated_at` in ticket and comment schemas
- CSV rows in [`src/backend/app/tickets/service.py`](src/backend/app/tickets/service.py) use `ensure_utc(...).isoformat()`

### Validation

- `uv run pytest -v` — 16/16 passed after the change
- Timestamps now serialize with UTC awareness (e.g. `...Z` or `+00:00`) so the browser converts to local correctly
