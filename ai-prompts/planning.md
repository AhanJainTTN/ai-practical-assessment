# Planning Prompts

## Entry 1 — Repo init file list (pre-stack)

### Prompt (text or summary)

Refer to the assessment PDF. Assuming tech stack is TBD and support ticket management system requirements are yet to be locked down, what all files should I be initialising the repository with?

### AI response summary

Proposed full PDF Required Repository Structure scaffold: root docs, `ai-prompts/`, `tool-specific/cursor-workflow/`, `src/`, `tests/`, `database/`, `.gitignore`; defer stack lock-in files; seed Core brief facts only.

### Accepted

Core-only scaffold; docs at root; no stack packages yet.

### Changed

(none yet in this turn)

### Rejected (and why)

Inventing frontend/backend lock-in files before stack decision.

## Entry 2 — Stretch out of scope

### Prompt (text or summary)

The optional part will be out of scope.

### AI response summary

Updated plan so Stretch is permanently excluded (auth, Docker, OpenAPI, user CRUD, richer model) — not deferred.

### Accepted

Stretch permanently out of scope in seeded docs and scaffold.

### Changed

Plan language from "Stretch later" to "never for this submission."

### Rejected (and why)

Scaffolding Stretch placeholders.

## Entry 3 — Follow Submission Templates

### Prompt (text or summary)

Refer to submission templates for structure.

### AI response summary

Rewrote plan so each markdown file uses exact PDF Submission Template section headers; remaining required files get minimal matching headers; `ai-prompts/` entries use PDF prompt-entry shape.

### Accepted

Template-exact section structure for all scaffolded docs.

### Changed

From generic "purpose table" to verbatim template headers in the plan.

### Rejected (and why)

Inventing extra top-level doc sections beyond templates/Part A.
