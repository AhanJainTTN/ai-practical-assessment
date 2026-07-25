# Data Model

## User

Seeded only — no user-management UI required.

| Field | Type | Notes |
|-------|------|-------|
| id | identifier | Primary key |
| name | string | Required |
| email | string | Required |
| role | enum | `requester` or `agent` — seed/display only; no permission checks in Core |

## Ticket

| Field | Type | Notes |
|-------|------|-------|
| id | identifier | Primary key |
| title | string | Required; non-empty |
| description | string | Required; non-empty |
| priority | enum | `Low`, `Medium`, `High` — required |
| status | enum | `Open`, `In Progress`, `Resolved`, `Closed`, `Cancelled` — new tickets start as `Open` |
| assignedTo | foreign key | Nullable; references User.id |
| createdBy | foreign key | Required; references User.id (Acting-as user on create) |
| createdAt | timestamp | Set on create |
| updatedAt | timestamp | Set on create and update |

## Comment

| Field | Type | Notes |
|-------|------|-------|
| id | identifier | Primary key |
| ticketId | foreign key | Required; references Ticket.id |
| message | string | Required; non-empty |
| createdBy | foreign key | Required; references User.id (Acting-as user) |
| createdAt | timestamp | Set on create |

Comments are allowed on tickets in any status (including Closed and Cancelled).

## Relationships

- User → Ticket (createdBy): one-to-many
- User → Ticket (assignedTo): one-to-many (nullable)
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

Title, description, priority, and assignee may be updated in any status. Status may only change through the transitions above.

## Validation Rules

**Ticket create**
- `title`: required, non-empty
- `description`: required, non-empty
- `priority`: required; must be `Low`, `Medium`, or `High`
- `status`: always `Open` (not client-supplied)
- `createdBy`: required; must reference an existing user
- `assignedTo`: optional; if provided, must reference an existing user

**Ticket update**
- Same field rules apply to any field sent
- `assignedTo` may be set to null (unassign)
- Status changes only via valid state-machine transitions

**Comment create**
- `ticketId`: required; must reference an existing ticket
- `message`: required, non-empty
- `createdBy`: required; must reference an existing user

## Seed Expectations

Minimum seed data for demo:

- **Users:** at least 3, with a mix of `requester` and `agent` roles
- **Tickets:** at least one per status (`Open`, `In Progress`, `Resolved`, `Closed`, `Cancelled`) to exercise list filter and state machine
- **Comments:** at least one ticket with comments
- **CSV demo:** at least 2 tickets created by the same user so export is non-trivial
