from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.comments.models import Comment
from app.comments.repository import CommentRepository
from app.comments.schemas import CommentCreate, CommentOut
from app.core.time import utcnow
from app.tickets.repository import TicketRepository
from app.users.repository import UserRepository
from app.users.schemas import UserRef


class CommentService:
    def __init__(self, db: Session) -> None:
        self.repository = CommentRepository(db)
        self.tickets = TicketRepository(db)
        self.users = UserRepository(db)

    def create_comment(self, ticket_id: int, payload: CommentCreate) -> CommentOut:
        if self.tickets.get_by_id_simple(ticket_id) is None:
            raise HTTPException(status_code=404, detail="Ticket not found")
        if self.users.get_by_id(payload.created_by) is None:
            raise HTTPException(status_code=422, detail="createdBy user does not exist")

        comment = Comment(
            ticket_id=ticket_id,
            message=payload.message,
            created_by=payload.created_by,
            created_at=utcnow(),
        )
        created = self.repository.add(comment)
        return CommentOut(
            id=created.id,
            message=created.message,
            created_by=UserRef.model_validate(created.creator),
            created_at=created.created_at,
        )
