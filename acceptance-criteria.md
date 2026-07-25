# Acceptance Criteria

## Core

- [ ] A user can create a ticket via the UI
- [ ] A user can view all tickets from the database
- [ ] A user can open a ticket detail view
- [ ] A user can update ticket fields and reassign
- [ ] A user can add comments
- [ ] Status changes only through valid transitions; invalid ones are rejected
- [ ] Data remains available after restart
- [ ] User can export all self-generated tickets with details as CSV
- [ ] One working search or filter capability

## Validation

- [ ] Backend validation prevents invalid records
- [ ] Required fields are validated on create/update
- [ ] Invalid status transitions are rejected by the backend

## Error Handling

- [ ] Meaningful error states are shown in the UI
- [ ] Invalid input from the backend is surfaced clearly to the user

## Testing

- [ ] State-machine integration tests pass
- [ ] Valid transitions succeed
- [ ] Invalid transitions are rejected

## Documentation

- [ ] README includes setup instructions that work locally
- [ ] Database setup/migration and seed data are documented
- [ ] Prompt history is captured under `ai-prompts/`
- [ ] No secrets committed to the repository
