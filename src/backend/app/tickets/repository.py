from sqlalchemy.orm import Session, joinedload, selectinload

from app.comments.models import Comment
from app.tickets.models import Ticket


class TicketRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self, status: str | None = None) -> list[Ticket]:
        query = (
            self.db.query(Ticket)
            .options(
                joinedload(Ticket.creator),
                joinedload(Ticket.assignee),
            )
            .order_by(Ticket.created_at.desc())
        )
        if status is not None:
            query = query.filter(Ticket.status == status)
        return query.all()

    def get_by_id(self, ticket_id: int) -> Ticket | None:
        return (
            self.db.query(Ticket)
            .options(
                joinedload(Ticket.creator),
                joinedload(Ticket.assignee),
                selectinload(Ticket.comments).joinedload(Comment.creator),
            )
            .filter(Ticket.id == ticket_id)
            .first()
        )

    def get_by_id_simple(self, ticket_id: int) -> Ticket | None:
        return (
            self.db.query(Ticket)
            .options(
                joinedload(Ticket.creator),
                joinedload(Ticket.assignee),
            )
            .filter(Ticket.id == ticket_id)
            .first()
        )

    def list_by_creator(self, created_by: int) -> list[Ticket]:
        return (
            self.db.query(Ticket)
            .options(
                joinedload(Ticket.creator),
                joinedload(Ticket.assignee),
                selectinload(Ticket.comments),
            )
            .filter(Ticket.created_by == created_by)
            .order_by(Ticket.created_at.desc())
            .all()
        )

    def add(self, ticket: Ticket) -> Ticket:
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def save(self, ticket: Ticket) -> Ticket:
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
