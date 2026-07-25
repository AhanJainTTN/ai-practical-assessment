# Test Strategy

## Test Scope

Core functionality for the Support Ticket Management System. Stretch/optional features are out of scope.

Mandatory: integration tests must prove state-machine rules (valid transitions succeed; invalid transitions are rejected).

## Unit Tests

TBD

## Component Tests

TBD

## API / Integration Tests

- Valid status transitions succeed (Open → In Progress, In Progress → Resolved, Resolved → Closed, Open → Cancelled, In Progress → Cancelled)
- Invalid status transitions are rejected by the backend

## Edge Case Tests

TBD

## Tests Not Covered (and why)

TBD
