# Design Prompts

## Entry 1 — Stack decision factors (2026-07-26)

### Prompt (text or summary)

Requirements are mostly locked. What should I keep in mind while deciding a tech stack?

### AI response summary

AI framed stack choice around assessment delivery (not production scale): familiarity over resume stacks, match complexity to Core scope, enforce business rules on the backend, keep FE↔BE contract simple (REST + JSON), prefer boring RDBMS with easy migrations/seeds, confirm pytest integration-test path works, document why for each layer, and avoid accidentally pulling Stretch back in.

### Accepted

- Decision filter: scaffold in under a day, known migrations/seeds/tests, obvious backend home for state machine, 5–10 README commands, defensible one-paragraph rationale
- Backend enforcement for transitions, enums, and FK checks

### Changed

- N/A — criteria applied in subsequent entries

### Rejected (and why)

- Production-ambition stacks (microservices, GraphQL, heavy auth kits) — overkill for Core CRUD + state machine
- Stretch-shaped tooling (Docker, OpenAPI generators, RBAC frameworks) — permanently out of scope

---

## Entry 2 — FastAPI + React shape (2026-07-26)

### Prompt (text or summary)

Considering scope and familiarity: Python BE, not Django (too much bloat), leaning FastAPI. React for FE. Does vanilla React make sense or should I use TypeScript / other variants?

### AI response summary

AI confirmed FastAPI + React as a solid Core fit. Recommended Vite + React SPA (not Next.js/CRA). JS vs TS based on familiarity — both valid; avoid Redux and heavy state libs. Suggested FastAPI + migrations/seeds + pytest on backend; React Router for three screens.

### Accepted

- **FastAPI** — lean Python API with Pydantic validation
- **Vite + React (JavaScript)** — SPA without SSR/meta-framework overhead
- **React Router** for list / create / detail

### Changed

- N/A

### Rejected (and why)

- **Django** — too much boilerplate for Core scope
- **Next.js / Remix** — unnecessary SSR and deployment complexity
- **CRA** — outdated starter
- **Redux / heavy state libs** — Acting-as + fetch state fits context/local state
- **TypeScript** — would slow delivery; not adopting mid-assessment to impress (OpenAPI client generation is Stretch anyway)

---

## Entry 3 — Linear look without shadcn (2026-07-26)

### Prompt (text or summary)

Would a Linear / shadcn-inspired UI change my FE choice? Follow-up: not committed to shadcn — just want the look to feel that way.

### AI response summary

AI explained Linear aesthetic is mostly CSS and layout discipline; shadcn implies Tailwind + Radix + TS. For Core, Vite + React stays correct. Without shadcn commitment, chase the vibe with neutral palette, compact rows, quiet badges, and a small CSS variables layer — no component library required.

### Accepted

- Lightweight CSS approach (variables + shared classes) for Linear-inspired look
- Status/priority as quiet badges; dense list rows; minimal chrome

### Changed

- N/A

### Rejected (and why)

- **shadcn/ui + Tailwind** — would push toward TS and extra deps; not committed
- **Next.js** for visual polish — look does not require a full-stack framework

---

## Entry 4 — SQLite and lock artifacts (2026-07-26)

### Prompt (text or summary)

FastAPI, React/Vite (JS) it is. SQLite will be fine — does the PDF require a specific RDBMS? Now that stack is finalised, create/update the necessary artefacts.

### AI response summary

AI confirmed PDF says "Use Any RDBMS" — SQLite is valid with documented migrate/seed/run steps. Planned and implemented documentation-only updates locking FastAPI + Vite/React (JS) + SQLite across README, design-notes, database/setup-notes, implementation-plan, test-strategy, api-contract outline, and related artifacts. Acting-as persistence set to `localStorage`.

### Accepted

- **SQLite** with SQLAlchemy + Alembic
- **localStorage** for Acting-as user
- Stack rationale recorded in design-notes and README
- REST API outline in api-contract.md

### Changed

- requirements-analysis NFRs and ui-flow updated for stack and Acting-as persistence
- api-contract sketched as next implementation step

### Rejected (and why)

- **Postgres** — SQLite sufficient for assessment; simpler reviewer setup
- App scaffolding in this session — docs only per plan; `src/` deferred to next milestone

---

## Entry 5 — Light UI/UX lock (2026-07-26)

### Prompt (text or summary)

Should I not lock the UI/UX before building? (Context from requirements chat: UI flow vs look are separate layers — flow locked in `ui-flow.md`; look comes after stack lock.)

### AI response summary

AI confirmed product UX is already locked in ui-flow.md. Recommended a short visual/interaction lock (tone, layout, badge style, error pattern, empty states) in design-notes — enough to avoid FE thrash — without a full design system, Figma, or component library gate before scaffold.

### Accepted

- Light visual direction: Linear-inspired dense list, muted borders, restrained badges
- Error pattern: banner for API/business errors; inline for field validation
- Pixel polish iterative during frontend milestone, not a separate gate

### Changed

- N/A — guidance applied during implementation

### Rejected (and why)

- Full design system / Figma mocks / hex palette dumps — wastes time before Core delivery
- Delaying backend scaffold for a design pass — build order should proceed

---

## Entry 6 — Linear dark reskin (2026-07-27)

### Prompt (text or summary)

The overall UI looks very basic. Refer to https://www.shadcn.io/design/linear for inspiration.

### AI response summary

AI reviewed current frontend and the Linear DESIGN.md reference. Planned and implemented a full dark reskin using Linear canvas tokens — near-black surfaces, lavender accent, Inter font, dense list/form chrome — with no new npm dependencies, matching existing design-notes.

### Accepted

- Dark canvas token system in `index.css` (`#010102` canvas, surface ladder, `#5e6ad2` accent)
- Inter via Google Fonts; lavender brand mark in header
- design-notes.md updated for dark Linear tokens

### Changed

- Replaced initial lighter Linear-inspired CSS from the first frontend pass

### Rejected (and why)

- **Tailwind / shadcn install** — aesthetic achievable without new deps; consistent with Entry 3
- Treating reskin as a reason to add a component library — kept hand-rolled CSS
