# Debugging Notes

## Issue 1 — Timestamp display skew (UTC vs local)

### Problem

After code review, ticket and comment timestamps in the list, detail view, and CSV appeared shifted from wall-clock time. In IST (UTC+5:30), a ticket created at 16:00 UTC could display as "4:00 PM" instead of "9:30 PM" — offset equal to the browser's UTC offset.

### How I Investigated

Traced the data path:

1. Backend writes UTC via `utcnow()` (`datetime.now(timezone.utc)`)
2. SQLite stores and returns **naive** datetimes (no offset)
3. API/CSV emitted `2026-07-27T16:00:00` with no `Z` or `+00:00`
4. Frontend `formatDateTime` calls `new Date(value)` — strings without timezone are parsed as **local** time

Confirmed sort order (`createdAt` desc), state machine, validation, and CSV filtering were unaffected — display-only bug.

### How AI Helped

AI explained practical impact (display/CSV only, not business logic) and compared fix options: backend serializer vs frontend `Z` append vs shared Pydantic type. Recommended `UtcDateTime` in `types.py` alongside `NonEmptyStr` to avoid scattering `as_utc()` across services. Clarified performance cost is negligible vs DB/JSON at any realistic Core scale.

### What I Validated

- Relative ordering of tickets/comments unchanged
- No acceptance-criteria failure — Core does not mandate timezone-correct display
- 16/16 pytest still pass after fix
- Timestamps now emit with UTC offset so `new Date` converts correctly

### Final Fix

- `ensure_utc()` in `src/backend/app/core/time.py`
- `UtcDateTime` annotated type in `src/backend/app/core/types.py`
- Response schemas and CSV export wired to use it

See [review-fixes.md](review-fixes.md) for file-level detail.
