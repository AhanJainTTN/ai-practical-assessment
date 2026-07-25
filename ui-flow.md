# UI Flow

## Screens

TBD — stack not yet locked. Expected screens:

1. **Ticket list** — view all tickets; search or filter
2. **Create ticket** — form for title, description, priority, assignee
3. **Ticket detail** — view and update ticket fields, change status, add comments, export CSV

## Ticket Lifecycle

```
Open ──→ In Progress ──→ Resolved ──→ Closed
  │            │
  └──→ Cancelled ←──┘
```

- Open → In Progress
- In Progress → Resolved
- Resolved → Closed
- Open → Cancelled
- In Progress → Cancelled

Invalid transitions must show a clear error in the UI.

## Error States

- Validation errors on create/update (required fields, invalid values)
- Invalid status transition rejected by backend
- General API/network failure messaging

## CSV Export

User can export all self-generated tickets with details as CSV. Export behavior and "current user" context TBD (no auth in Core scope).
