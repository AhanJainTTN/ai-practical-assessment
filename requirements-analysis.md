# Requirement Analysis

## Selected Project Option

Support Ticket Management System (Core only).

Stretch/optional features are deliberately excluded from scope.

## My Understanding (in your own words)

A small internal application for managing support tickets. Internal users create, update, comment on, search, and progress tickets through a defined lifecycle. Users are seeded only — no user-management UI is required.

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

## Non-Functional Requirements

- Frontend application (any JS library) — stack TBD
- Backend API (any Python framework) — stack TBD
- Database persistence (any RDBMS) — choice TBD
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
- "Self-generated tickets" for CSV export refers to tickets created by the current user context (TBD how user context is represented without auth)

## Clarifications (questions for a product owner)

- How is the "current user" determined for CSV export without authentication?
- What are the allowed priority values?
- What search/filter fields are required (title, status, priority, assignee)?
- What user roles exist in seed data and do they affect behavior?

## Edge Cases

- Attempting invalid status transitions (must be rejected)
- Missing or empty required fields on create/update
- Commenting on non-existent tickets
- Assigning to non-existent users
- Exporting when no tickets exist
- Data persistence across application restart
