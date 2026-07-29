# API Contract

Base URL: `http://localhost:8000` (local dev). All JSON responses unless noted. Error shape follows FastAPI conventions.

## Shared error responses

| Status | When | Body |
|--------|------|------|
| 422 | Validation failure | `{ "detail": [ { "loc": [...], "msg": "...", "type": "..." } ] }` |
| 400 | Business rule failure (e.g. invalid transition) | `{ "detail": "..." }` |
| 404 | Resource not found | `{ "detail": "..." }` |

---

## GET /api/users

**Purpose:** List seeded users for Acting-as selector and assignee dropdown.

### Response

```json
[
  { "id": 1, "name": "...", "email": "...", "role": "requester" }
]
```

---

## GET /api/tickets

**Purpose:** List all tickets; optional status filter. Default sort: `createdAt` descending.

### Query parameters

| Param | Type | Notes |
|-------|------|-------|
| `status` | string | Optional. One of `Open`, `In Progress`, `Resolved`, `Closed`, `Cancelled`. Omit for all. |

### Response

```json
[
  {
    "id": 1,
    "title": "...",
    "description": "...",
    "priority": "Medium",
    "status": "Open",
    "assignedTo": { "id": 2, "name": "...", "email": "..." },
    "createdBy": { "id": 1, "name": "...", "email": "..." },
    "createdAt": "2026-01-01T00:00:00",
    "updatedAt": "2026-01-01T00:00:00"
  }
]
```

`assignedTo` may be `null`.

---

## POST /api/tickets

**Purpose:** Create a ticket. Status is always `Open` (server-set).

### Request

```json
{
  "title": "string",
  "description": "string",
  "priority": "Low | Medium | High",
  "createdBy": 1,
  "assignedTo": 2
}
```

`assignedTo` optional (omit or `null` for unassigned).

### Validation rules

- `title`, `description`: required, non-empty
- `priority`: required; must be `Low`, `Medium`, or `High`
- `createdBy`: required; must reference existing user
- `assignedTo`: optional; if provided, must reference existing user
- `status`: not accepted from client; always `Open`

### Response

`201` — created ticket object (same shape as list item).

---

## GET /api/tickets/{id}

**Purpose:** Ticket detail including comments.

### Response

```json
{
  "id": 1,
  "title": "...",
  "description": "...",
  "priority": "Medium",
  "status": "Open",
  "assignedTo": null,
  "createdBy": { "id": 1, "name": "...", "email": "..." },
  "createdAt": "...",
  "updatedAt": "...",
  "comments": [
    {
      "id": 1,
      "message": "...",
      "createdBy": { "id": 1, "name": "...", "email": "..." },
      "createdAt": "..."
    }
  ]
}
```

### Error responses

- `404` if ticket not found

---

## PATCH /api/tickets/{id}

**Purpose:** Update ticket fields (not status). Title, description, priority, assignee editable in any status.

### Request

Partial update — only include fields to change:

```json
{
  "title": "string",
  "description": "string",
  "priority": "High",
  "assignedTo": null
}
```

### Validation rules

- Same field rules as create for any field sent
- `assignedTo` may be `null` to unassign
- Status changes are **not** allowed on this endpoint

### Response

`200` — updated ticket object.

### Error responses

- `404` if ticket not found
- `422` for invalid priority or non-existent assignee

---

## POST /api/tickets/{id}/transitions

**Purpose:** Change ticket status via state machine only.

### Request

```json
{
  "status": "In Progress"
}
```

### Allowed transitions

| From | To |
|------|-----|
| Open | In Progress, Cancelled |
| In Progress | Resolved, Cancelled |
| Resolved | Closed |

All other transitions → `400`.

### Response

`200` — updated ticket object with new status.

### Error responses

- `404` if ticket not found
- `400` if transition is invalid

---

## POST /api/tickets/{id}/comments

**Purpose:** Add a comment to a ticket (any ticket status, including Closed/Cancelled).

### Request

```json
{
  "message": "string",
  "createdBy": 1
}
```

### Validation rules

- `message`: required, non-empty
- `createdBy`: required; must reference existing user
- `ticketId` implied from path; ticket must exist

### Response

`201` — created comment object.

### Error responses

- `404` if ticket not found
- `422` for empty message or invalid `createdBy`

---

## GET /api/tickets/export.csv

**Purpose:** Export self-generated tickets as CSV for the Acting-as user.

### Query parameters

| Param | Type | Notes |
|-------|------|-------|
| `createdBy` | integer | Required. User id — export tickets where `createdBy` matches. |

### Response

`200` — `text/csv` attachment.

Columns (per [ui-flow.md](ui-flow.md)): `id`, `title`, `description`, `priority`, `status`, assignee name, assignee email, creator name, creator email, `createdAt`, `updatedAt`, `commentCount`, `comments` (messages joined with ` | `).

If no matching tickets: CSV with headers only (success, not an error).

### Error responses

- `422` if `createdBy` missing or invalid user
