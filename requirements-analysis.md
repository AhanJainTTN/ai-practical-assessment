# Requirement Analysis

## Selected Project Option

Support Ticket Management System (Core only).

Stretch/optional features are deliberately excluded from scope.

## My Understanding (in your own words)

A small internal application for managing support tickets. Internal users create, update, comment on, search, and progress tickets through a defined lifecycle. Users are seeded only — no user-management UI is required.

Without authentication, the app uses an **Acting as** user selector so create, comment, and CSV export actions have a consistent "current user" context.

## Functional Requirements

From the assessment brief (Core):

1. Create a ticket
2. List tickets
3. View ticket details
4. Update ticket fields (title, description, priority, assignee)
5. Change ticket status through the enforced state machine
6. Add comments to a ticket
7. Persist all data; data survives restart
8. Validate required fields; reject invalid input at the backend
9. Show meaningful error states in the UI
10. Export all self-generated tickets with details as CSV
11. One working search or filter capability

### Entities

**User** (seeded only)
- id, name, email, role

**Ticket**
- id, title, description, priority, status, assignedTo, createdBy, createdAt, updatedAt

**Comment**
- id, ticketId, message, createdBy, createdAt

### Status state machine

Allowed transitions:
- Open → In Progress
- In Progress → Resolved
- Resolved → Closed
- Open → Cancelled
- In Progress → Cancelled

Invalid transitions must be rejected by the backend and handled clearly in the frontend.

### Locked product behaviors (Core)

- **Acting as user:** App-wide dropdown of seeded users (required for create, comment, and CSV export). Client-only persistence; no login.
- **Priority:** `Low`, `Medium`, `High` — required on create; default `Medium` in the UI.
- **Search/filter:** Exactly one capability — **filter by status** on the ticket list (`All` + each status value). No title search in Core.
- **CSV export:** On the ticket list; exports tickets where `createdBy` equals the Acting-as user. See `ui-flow.md` for columns and empty-result behavior.
- **Create defaults:** New tickets start as `Open`; `createdBy` = Acting-as user; `assignedTo` optional (nullable).
- **Field updates:** Title, description, priority, and assignee editable in any status. Status changes only via the state machine. No ticket delete in Core.
- **Comments:** Allowed on any existing ticket (including Closed/Cancelled).
- **List behavior:** All tickets, no pagination; default sort `createdAt` descending.

## Non-Functional Requirements

- Frontend: Vite + React (JavaScript) SPA
- Backend API: FastAPI (Python)
- Database persistence: SQLite (any RDBMS allowed by brief)
- Database setup or migration scripts
- Seed or sample data
- Input validation and error handling
- At least one meaningful test tier (mandatory state-machine integration tests)
- README setup instructions
- Prompt history (Cursor chat exports)
- No secrets committed to the repository

## Assumptions

- Internal users only; no authentication required (Stretch auth is out of scope)
- Users are pre-seeded; no user CRUD UI
- **Acting as user** represents the current user context without auth. It is required before create, comment, or CSV export. Selection persists in browser `localStorage`.
- **Self-generated tickets** for CSV export means tickets where `createdBy` matches the Acting-as user
- **Priority** values are `Low`, `Medium`, `High` only; backend rejects other values
- **Roles** (`requester`, `agent`) are seed/display metadata only — no permission checks, UI gating, or API authorization in Core
- **Assignee** (`assignedTo`) is optional; tickets may be unassigned
- **New tickets** always start with status `Open`; creator is the Acting-as user (not editable on the form)
- **Required fields:** ticket create requires non-empty title, non-empty description, and priority; comment requires non-empty message
- **Status filter** is the single search/filter capability; no title, priority, or assignee filter in Core
- **No ticket delete** in Core
- **Seed data** includes at least 3 users (mix of roles), tickets covering each status for demo, at least one ticket with comments, and at least 2 tickets created by one user for non-trivial CSV export

## Resolved clarifications

| Question | Decision | Rationale |
|----------|----------|-----------|
| How is the "current user" determined for CSV export without authentication? | App-wide **Acting as** dropdown of seeded users; used for `createdBy` on create/comment and CSV filter | One concept covers create, comment, and export without Stretch auth |
| What are the allowed priority values? | `Low`, `Medium`, `High` — required on create; default `Medium` in UI | Small familiar set; enough to demo validation |
| What search/filter fields are required? | **Status filter only** on ticket list (`All` + each status) | Exactly one capability per brief; reinforces state machine |
| What user roles exist in seed data and do they affect behavior? | `requester` and `agent` — **display/seed only**; no behavioral effect in Core | Brief requires `role` on User; RBAC is Stretch |
| What is the technology stack? | **FastAPI** backend, **Vite + React (JS)** frontend, **SQLite** database; SQLAlchemy + Alembic for schema/seed; pytest for state-machine tests | Familiar, lean stack sized for Core scope; no Django/Next/Docker/auth overhead |
| How is Acting-as user persisted? | Browser **`localStorage`** | Client-only; survives refresh; no auth |

No open Core product or stack clarifications remain. Tech stack is locked.

## Edge Cases

- Attempting invalid status transitions (must be rejected by backend; clear error in UI)
- Missing or empty required fields on create/update (title, description, priority, comment message)
- Invalid priority value (must be rejected)
- Commenting on non-existent tickets (must be rejected)
- Assigning to non-existent users (must be rejected)
- Acting-as user not selected before create, comment, or export (UI blocks or prompts selection)
- Exporting when Acting-as user has no tickets (CSV with headers only — success, not an error)
- Comments allowed on Closed/Cancelled tickets
- Data persistence across application restart
