import csv
import io

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.time import utcnow
from app.tickets.models import Ticket
from app.tickets.repository import TicketRepository
from app.tickets.schemas import (
    TicketCreate,
    TicketDetailOut,
    TicketOut,
    TicketStatus,
    TicketUpdate,
)
from app.comments.schemas import CommentOut
from app.users.repository import UserRepository
from app.users.schemas import UserRef

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "Open": {"In Progress", "Cancelled"},
    "In Progress": {"Resolved", "Cancelled"},
    "Resolved": {"Closed"},
    "Closed": set(),
    "Cancelled": set(),
}

VALID_STATUSES = frozenset(ALLOWED_TRANSITIONS.keys())

CSV_HEADERS = [
    "id",
    "title",
    "description",
    "priority",
    "status",
    "assigneeName",
    "assigneeEmail",
    "creatorName",
    "creatorEmail",
    "createdAt",
    "updatedAt",
    "commentCount",
    "comments",
]


def _user_ref(user) -> UserRef:
    return UserRef.model_validate(user)


def _ticket_out(ticket: Ticket) -> TicketOut:
    return TicketOut(
        id=ticket.id,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        status=ticket.status,
        assigned_to=_user_ref(ticket.assignee) if ticket.assignee else None,
        created_by=_user_ref(ticket.creator),
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
    )


def _ticket_detail_out(ticket: Ticket) -> TicketDetailOut:
    comments = sorted(ticket.comments, key=lambda c: (c.created_at, c.id))
    base = _ticket_out(ticket)
    return TicketDetailOut(
        **base.model_dump(),
        comments=[
            CommentOut(
                id=comment.id,
                message=comment.message,
                created_by=_user_ref(comment.creator),
                created_at=comment.created_at,
            )
            for comment in comments
        ],
    )


class TicketService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = TicketRepository(db)
        self.users = UserRepository(db)

    def list_tickets(self, status: str | None = None) -> list[TicketOut]:
        if status is not None and status not in VALID_STATUSES:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid status filter: {status}",
            )
        tickets = self.repository.list_all(status=status)
        return [_ticket_out(ticket) for ticket in tickets]

    def get_ticket(self, ticket_id: int) -> TicketDetailOut:
        ticket = self.repository.get_by_id(ticket_id)
        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return _ticket_detail_out(ticket)

    def create_ticket(self, payload: TicketCreate) -> TicketOut:
        if self.users.get_by_id(payload.created_by) is None:
            raise HTTPException(status_code=422, detail="createdBy user does not exist")
        if payload.assigned_to is not None and self.users.get_by_id(payload.assigned_to) is None:
            raise HTTPException(status_code=422, detail="assignedTo user does not exist")

        now = utcnow()
        ticket = Ticket(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status="Open",
            created_by=payload.created_by,
            assigned_to=payload.assigned_to,
            created_at=now,
            updated_at=now,
        )
        self.repository.add(ticket)
        created = self.repository.get_by_id_simple(ticket.id)
        assert created is not None
        return _ticket_out(created)

    def update_ticket(self, ticket_id: int, payload: TicketUpdate) -> TicketOut:
        ticket = self.repository.get_by_id_simple(ticket_id)
        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")

        updates = payload.model_dump(exclude_unset=True)
        if "assigned_to" in updates and updates["assigned_to"] is not None:
            if self.users.get_by_id(updates["assigned_to"]) is None:
                raise HTTPException(status_code=422, detail="assignedTo user does not exist")

        for field, value in updates.items():
            setattr(ticket, field, value)

        ticket.updated_at = utcnow()
        self.repository.save(ticket)
        updated = self.repository.get_by_id_simple(ticket_id)
        assert updated is not None
        return _ticket_out(updated)

    def transition_ticket(self, ticket_id: int, status: TicketStatus) -> TicketOut:
        ticket = self.repository.get_by_id_simple(ticket_id)
        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")

        allowed = ALLOWED_TRANSITIONS.get(ticket.status, set())
        if status not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid transition from {ticket.status} to {status}",
            )

        ticket.status = status
        ticket.updated_at = utcnow()
        self.repository.save(ticket)
        updated = self.repository.get_by_id_simple(ticket_id)
        assert updated is not None
        return _ticket_out(updated)

    def export_csv(self, created_by: int) -> str:
        if self.users.get_by_id(created_by) is None:
            raise HTTPException(status_code=422, detail="createdBy user does not exist")

        tickets = self.repository.list_by_creator(created_by)
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(CSV_HEADERS)

        for ticket in tickets:
            comments = sorted(ticket.comments, key=lambda c: (c.created_at, c.id))
            writer.writerow(
                [
                    ticket.id,
                    ticket.title,
                    ticket.description,
                    ticket.priority,
                    ticket.status,
                    ticket.assignee.name if ticket.assignee else "",
                    ticket.assignee.email if ticket.assignee else "",
                    ticket.creator.name,
                    ticket.creator.email,
                    ticket.created_at.isoformat(),
                    ticket.updated_at.isoformat(),
                    len(comments),
                    " | ".join(comment.message for comment in comments),
                ]
            )

        return buffer.getvalue()
