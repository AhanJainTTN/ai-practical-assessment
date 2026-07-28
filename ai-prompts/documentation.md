# Documentation Prompts

## Entry 1 — Lock stack across assessment artifacts (2026-07-26)

### Prompt (text or summary)

Now that the tech stack / rationale is finalised (FastAPI, Vite/React JS, SQLite), create / update the necessary artefacts. Documentation only — no app scaffolding.

### AI response summary

AI planned and applied documentation-only updates locking the stack across README, candidate-info, requirements-analysis (NFRs), ui-flow (Acting-as `localStorage`), design-notes, database/setup-notes, implementation-plan, test-strategy, and a REST outline in api-contract.md. Prompt history entries appended under `ai-prompts/`.

### Accepted

- Stack table and rationale in README and design-notes
- Acting-as persistence documented as `localStorage`
- pytest + TestClient approach in test-strategy.md
- Docs-only session — `src/` deferred to next milestone

### Changed

- Replaced “stack TBD” language across identity, plan, DB, and NFR docs

### Rejected (and why)

- Scaffolding application code in this session — scope was artifacts and rationale only
- Inventing product requirements during stack lock — Core product decisions already locked

---

## Entry 2 — Align api-contract timestamps (2026-07-26)

### Prompt (text or summary)

After rejecting `Z`-suffix serializers on the API: “Updated `@api-contract.md` to reflect this as well.”

### AI response summary

On disk the contract still showed `Z` examples. AI updated list-response timestamp examples to match Pydantic’s default ISO serialization (no `Z`), so the contract documents what the API actually returns.

### Accepted

- Contract examples updated to match live API output
- Documentation follows implementation judgment (no serializer overhead for cosmetic `Z`)

### Changed

- Timestamp examples in `api-contract.md` list responses

### Rejected (and why)

- Keeping contract `Z` examples while the API omitted them — would document aspirational format, not reality
- Re-introducing field serializers just to satisfy old examples — already rejected in implementation

---

## Entry 3 — Finalize test and delivery docs (2026-07-27)

### Prompt (text or summary)

Finish remaining implementation-plan steps (state-machine tests plus assessment doc polish).

### AI response summary

After the 16-test suite passed, AI filled `test-results.md`, checked off `acceptance-criteria.md`, drafted `pr-description.md`, logged the testing prompt in `ai-prompts/testing.md`, and updated the README test section.

### Accepted

- test-results.md with run summary and coverage of state-machine + validation cases
- acceptance-criteria.md fully checked for Core
- pr-description.md as single final delivery write-up
- README test commands reflecting the live pytest suite

### Changed

- README wording no longer deferred (“after tests are added”)

### Rejected (and why)

- Filling `pr-description.md` per intermediate commit/PR — kept as one submission artifact for the main delivery
- Expanding docs into Stretch (auth, Docker, OpenAPI) — Core-only
