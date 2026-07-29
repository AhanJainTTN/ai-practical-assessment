# UI Flow

## App Chrome

- **Acting as** user selector (dropdown of seeded users) — visible app-wide
- Required before create ticket, add comment, or CSV export
- Selection persists in browser `localStorage` between visits
- If not selected, mutating actions and export are blocked or prompt selection

## Screens

1. **Ticket list** — view all tickets; status filter; create entry point; CSV export
2. **Create ticket** — form for title, description, priority, optional assignee
3. **Ticket detail** — view and update ticket fields, change status, add comments

## Ticket List

- Shows all tickets from the database (no pagination)
- Default sort: `createdAt` descending (newest first)
- **Status filter** (single search/filter capability): `All`, `Open`, `In Progress`, `Resolved`, `Closed`, `Cancelled`
- Each row links to ticket detail
- **Create ticket** action navigates to create form
- **Export CSV** action exports self-generated tickets for the Acting-as user (see CSV Export below)
- No CSV export on the detail screen

## Create Ticket

- Fields: title (required), description (required), priority (required; default `Medium`), assignee (optional dropdown of seeded users)
- Creator (`createdBy`) = Acting-as user — shown as read-only indication optional; not editable on form
- New ticket status is always `Open` (not user-selectable)
- Submit creates ticket and navigates to detail or back to list
- Validation errors from backend shown inline or as banner

## Ticket Detail

- View all ticket fields including status, creator, assignee, timestamps
- Edit title, description, priority, assignee (in any status)
- **Status control:** offers only valid next statuses per state machine; invalid transitions show backend error
- **Comments:** list existing comments (author, message, timestamp); form to add comment (message required; `createdBy` = Acting-as)
- Comments allowed regardless of ticket status (including Closed/Cancelled)
- No delete ticket action in Core
- No CSV export on this screen

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

- Validation errors on create/update (required fields, invalid priority, invalid assignee)
- Invalid status transition rejected by backend
- Acting-as user not selected before create, comment, or export
- Comment on non-existent ticket (API error surfaced)
- General API/network failure messaging

## CSV Export

- **Location:** ticket list only
- **Trigger:** Export CSV control (requires Acting-as user selected)
- **Filter:** tickets where `createdBy` = Acting-as user
- **Format:** one row per ticket; columns:
  - `id`, `title`, `description`, `priority`, `status`
  - assignee name, assignee email (empty if unassigned)
  - creator name, creator email
  - `createdAt`, `updatedAt`
  - `commentCount`
  - `comments` — all comment messages joined with ` | `
- **Empty result:** download CSV with headers only (success, not an error)
