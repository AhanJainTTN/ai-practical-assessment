# Acceptance Criteria

## Core

- [x] Acting-as user can be selected from seeded users (required for create, comment, export)
- [x] A user can create a ticket via the UI (title, description, priority required; status starts Open; assignee optional; `createdBy` = Acting-as user)
- [x] A user can view all tickets from the database (default sort: `createdAt` descending; no pagination)
- [x] Ticket list has a **status filter** (`All` + each status value) — the single search/filter capability
- [x] A user can open a ticket detail view
- [x] A user can update ticket fields (title, description, priority, assignee) in any status
- [x] A user can add comments (message required; `createdBy` = Acting-as user; allowed on any ticket status)
- [x] Status changes only through valid transitions; UI offers only valid next statuses; invalid ones are rejected
- [x] Data remains available after restart
- [x] User can export self-generated tickets as CSV from the ticket list (only tickets where `createdBy` = Acting-as user; agreed columns; header-only CSV when none exist)
- [x] Priority is limited to `Low`, `Medium`, `High`
- [x] User roles (`requester`, `agent`) do not change available actions

## Validation

- [x] Backend validation prevents invalid records
- [x] Required fields are validated on create/update (title, description, priority on ticket; message on comment)
- [x] Invalid priority values are rejected by the backend
- [x] Invalid status transitions are rejected by the backend
- [x] Assigning to a non-existent user is rejected by the backend
- [x] Commenting on a non-existent ticket is rejected by the backend

## Error Handling

- [x] Meaningful error states are shown in the UI
- [x] Invalid input from the backend is surfaced clearly to the user
- [x] Acting-as user not selected is handled clearly before create, comment, or export

## Testing

- [x] State-machine integration tests pass
- [x] Valid transitions succeed (Open → In Progress, In Progress → Resolved, Resolved → Closed, Open → Cancelled, In Progress → Cancelled)
- [x] Invalid transitions are rejected

## Documentation

- [x] README includes setup instructions that work locally
- [x] Database setup/migration and seed data are documented
- [x] Prompt history is captured under `ai-prompts/`
- [x] No secrets committed to the repository
