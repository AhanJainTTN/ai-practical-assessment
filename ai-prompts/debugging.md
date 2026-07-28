# Debugging Prompts

## Entry 1 — Timezone display skew after review (2026-07-28)

### Prompt (text or summary)

Follow-up to code review nit on naive UTC timestamps: "What is the practical impact of the timezone issue?" Then: "How would this be fixed with minimal performance impact?" Then: "Would I be duplicating logic everywhere — why not a Pydantic type like `NonEmptyStr` in types.py?" Then: "Performance impact if I ignore CSV, at scale?" Finally: "Implement it."

### AI response summary

AI traced `utcnow` → SQLite naive → API/CSV → `new Date` local parsing. Impact: display-only skew (~5.5h in IST), not logic bugs. Recommended shared `UtcDateTime` with `AfterValidator(ensure_utc)` in `types.py` plus `ensure_utc` for CSV rows only. Explained sub-microsecond per-field cost vs DB/JSON dominance. Implemented `ensure_utc`, `UtcDateTime`, schema wiring, and CSV path; all 16 tests passed.

### Accepted

- Shared `UtcDateTime` type mirroring `NonEmptyStr` pattern (single definition, reuse on response fields)
- `ensure_utc()` helper reused from CSV export (Pydantic does not serialize CSV rows)
- Backend fix (covers API + CSV) over frontend-only `Z` append

### Changed

- N/A — initial review left timezone as optional nit; promoted to fix after impact analysis

### Rejected (and why)

- Scattering `as_utc()` in every service/build path — duplication; centralized in `types.py` instead
- New timezone library — unnecessary for Core
- Frontend-only fix — would not correct CSV `isoformat()` strings
- Earlier `to_iso_z()` field serializers (implementation Entry 4) — had been rejected as overhead; this fix uses a shared type for a concrete display bug found in review
