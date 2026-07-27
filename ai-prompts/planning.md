# Planning Prompts

## Entry 1 — Repo init scaffold (2026-07-25)

### Prompt (text or summary)

Refer to the assessment PDF. Assuming tech stack is TBD and support ticket management requirements are yet to be locked down, what files should I initialise the repository with? Follow-up: mark Stretch/optional work as out of scope; align scaffolds to PDF submission templates exactly.

### AI response summary

AI reviewed the PDF required repo layout and drafted an init plan: root lifecycle docs, `ai-prompts/` by activity, `tool-specific/cursor-workflow/`, empty `src/` / `tests/` / `database/` placeholders, Core brief pre-seeding in requirements/data-model/ui-flow docs, and `.gitignore`. After scope tightening, Stretch was marked permanently out of scope (no Docker, auth, OpenAPI, user CRUD UI). Implementation created 18 root docs, directories, and pre-seeded Core content from the brief.

### Accepted

- PDF-aligned submission template structure for named artifacts
- Core-only scope with Stretch permanently excluded
- `ai-prompts/` with seven activity files using the PDF entry template
- Empty app/database placeholders until stack lock
- Pre-seeded requirements, acceptance criteria, data model, ui-flow, implementation plan

### Changed

- Scope language tightened after my "optional part will be out of scope" follow-up — file list unchanged, Stretch wording made explicit

### Rejected (and why)

- Stretch/optional features — permanently out of scope per assessment focus on Core only
- Stack-specific files (`package.json`, `requirements.txt`, Docker) — deferred until requirements and stack are locked

---

## Entry 2 — One final PR description (2026-07-25)

### Prompt (text or summary)

Should `pr-description.md` contain one final PR or every PR created? What if I commit now when done with scaffolding?

### AI response summary

AI advised treating `pr-description.md` as a single submission artifact describing the final delivery PR, not a log of every commit or intermediate PR. Scaffolding commits are fine as normal workflow; leave `pr-description.md` empty until Core is complete.

### Accepted

- One `pr-description.md` written at the end for the main delivery PR
- Many small commits for ownership (scaffold → requirements → API → UI → tests → docs)

### Changed

- N/A

### Rejected (and why)

- Per-PR or per-commit entries in `pr-description.md` — PDF template is singular and reviewers want one delivery narrative

---

## Entry 3 — Chat and phase sequencing (2026-07-25)

### Prompt (text or summary)

Should I use a new chat for locking down requirements and tech stack? Lock down stack first or requirements?

### AI response summary

AI recommended a fresh chat for the next phase (cleaner lifecycle evidence for `ai-prompts/`). On ordering: requirements first, then stack — product clarifications (priority values, Acting-as without auth, filter scope) shape the API more than framework choice; the PDF already constrains JS + Python + RDBMS families.

### Accepted

- Separate chat sessions per lifecycle phase
- Requirements lock before stack lock
- Attach brief PDF and seeded docs when starting the requirements chat

### Changed

- N/A

### Rejected (and why)

- Stack-first ordering — risks reverse-fitting product to framework and weaker requirement-analysis evidence

---

## Entry 4 — Lock Core requirements (2026-07-26)

### Prompt (text or summary)

Lock Core product/requirements decisions only — no tech stack. Read `@ai_assessment_plan.pdf`, `requirements-analysis.md`, `acceptance-criteria.md`, `data-model.md`, `ui-flow.md`. Resolve every clarification and assumption with concrete, demonstrable defaults.

### AI response summary

AI read the seeded docs and PDF brief, proposed simple product defaults, and updated all four requirements artifacts. Core product decisions locked; only tech stack and Acting-as persistence mechanism remained TBD.

### Accepted

- **Acting as** — seeded-user dropdown for create, comment, and CSV export (no auth)
- **Priority** — `Low` / `Medium` / `High` (required; default Medium)
- **Filter** — status only on ticket list (`All` + each status)
- **Roles** — `requester` / `agent`, display-only (no RBAC)
- **CSV** — from list; `createdBy` = Acting-as; defined columns; headers-only when empty
- **Create** — always `Open`; assignee optional; no delete in Core

### Changed

- Expanded assumptions, clarifications table, edge cases, and checkable acceptance criteria across the four docs

### Rejected (and why)

- Tech stack choices in this session — explicitly deferred to a separate stack-lock chat
- RBAC or role-based transition guards — kept roles display-only to keep Core small
