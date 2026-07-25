# Acceptance Criteria

## Core

- [ ] Acting-as user can be selected from seeded users (required for create, comment, export)
- [ ] A user can create a ticket via the UI (title, description, priority required; status starts Open; assignee optional; `createdBy` = Acting-as user)
- [ ] A user can view all tickets from the database (default sort: `createdAt` descending; no pagination)
- [ ] Ticket list has a **status filter** (`All` + each status value) — the single search/filter capability
- [ ] A user can open a ticket detail view
- [ ] A user can update ticket fields (title, description, priority, assignee) in any status
- [ ] A user can add comments (message required; `createdBy` = Acting-as user; allowed on any ticket status)
- [ ] Status changes only through valid transitions; UI offers only valid next statuses; invalid ones are rejected
- [ ] Data remains available after restart
- [ ] User can export self-generated tickets as CSV from the ticket list (only tickets where `createdBy` = Acting-as user; agreed columns; header-only CSV when none exist)
- [ ] Priority is limited to `Low`, `Medium`, `High`
- [ ] User roles (`requester`, `agent`) do not change available actions

## Validation

- [ ] Backend validation prevents invalid records
- [ ] Required fields are validated on create/update (title, description, priority on ticket; message on comment)
- [ ] Invalid priority values are rejected by the backend
- [ ] Invalid status transitions are rejected by the backend
- [ ] Assigning to a non-existent user is rejected by the backend
- [ ] Commenting on a non-existent ticket is rejected by the backend

## Error Handling

- [ ] Meaningful error states are shown in the UI
- [ ] Invalid input from the backend is surfaced clearly to the user
- [ ] Acting-as user not selected is handled clearly before create, comment, or export

## Testing

- [ ] State-machine integration tests pass
- [ ] Valid transitions succeed (Open → In Progress, In Progress → Resolved, Resolved → Closed, Open → Cancelled, In Progress → Cancelled)
- [ ] Invalid transitions are rejected

## Documentation

- [ ] README includes setup instructions that work locally
- [ ] Database setup/migration and seed data are documented
- [ ] Prompt history is captured under `ai-prompts/`
- [ ] No secrets committed to the repository
