# Data Model

## User

Seeded only — no user-management UI required.

| Field | Type | Notes |
|-------|------|-------|
| id | identifier | Primary key |
| name | string | |
| email | string | |
| role | string | TBD — allowed values to be confirmed |

## Ticket

| Field | Type | Notes |
|-------|------|-------|
| id | identifier | Primary key |
| title | string | Required |
| description | string | |
| priority | string | TBD — allowed values to be confirmed |
| status | enum | Open, In Progress, Resolved, Closed, Cancelled |
| assignedTo | foreign key | References User.id |
| createdBy | foreign key | References User.id |
| createdAt | timestamp | |
| updatedAt | timestamp | |

## Comment

| Field | Type | Notes |
|-------|------|-------|
| id | identifier | Primary key |
| ticketId | foreign key | References Ticket.id |
| message | string | Required |
| createdBy | foreign key | References User.id |
| createdAt | timestamp | |

## Relationships

- User → Ticket (createdBy): one-to-many
- User → Ticket (assignedTo): one-to-many
- User → Comment (createdBy): one-to-many
- Ticket → Comment: one-to-many

## Status State Machine

Allowed transitions:

| From | To |
|------|-----|
| Open | In Progress |
| In Progress | Resolved |
| Resolved | Closed |
| Open | Cancelled |
| In Progress | Cancelled |

All other transitions are invalid and must be rejected by the backend.
