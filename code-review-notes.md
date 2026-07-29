# Code Review Notes

## AI-Assisted Review Summary

Pre-submission review (chat 9) against `acceptance-criteria.md`, `api-contract.md`, and the backend/frontend/test trees. Verdict: **Core requirements met** — all eight endpoints, camelCase aliases, state machine on the server, Acting-as gating, CSV columns and header-only export, validation and error codes align with the contract. No blockers or should-fix items.

Nits flagged:

- Naive UTC timestamps serialized without offset (SQLite + `new Date` → local-time skew in UI/CSV)
- FE `ALLOWED_TRANSITIONS` mirror in `constants.js` (correct today; drift risk, no test guard)
- `allow_credentials=True` on CORS without auth/cookies in Core
- PATCH silently ignores unknown fields (e.g. `status`) — behavior is correct per contract

## My Review Observations

I treated the timezone nit as **display-only** before fixing: in IST, times could appear ~5.5 hours early because naive ISO strings are parsed as local. Sort order, state machine, and CSV filtering are unaffected. I asked for practical impact and performance-at-scale analysis before implementing anything.

I intentionally left most nits unchanged: the FE/BE transition map is needed to render buttons; redundant post-create re-queries load relationships for the response shape; invalid status filter returning `422` is sensible defensive validation beyond the contract.

## Changes Made After Review

Implemented one fix — shared UTC serialization:

- `ensure_utc()` in `src/backend/app/core/time.py`
- `UtcDateTime` in `src/backend/app/core/types.py` (mirrors `NonEmptyStr` pattern)
- Response `created_at` / `updated_at` on `TicketOut` and `CommentOut`
- CSV export uses `ensure_utc(...).isoformat()`

Left unchanged: CORS credentials, PATCH `extra` policy, FE transition map duplication.

## Suggestions Rejected (and why)

- **New endpoint for transition map** — exceeds Core minimalism; FE mirror is acceptable with a comment
- **`extra="forbid"` on PATCH** — silent ignore of `status` on PATCH is already correct; no requirement to reject unknown fields
- **`allow_credentials=False`** — low priority; origins are allowlisted, not a security issue for Core
- **Over-correcting “intentionally minimal” items** — redundant re-queries, comment router prefix, test scope — all adequate for Core
