from sqlalchemy.orm import Session

from app.comments.repository import CommentRepository


class CommentService:
    def __init__(self, db: Session) -> None:
        self.repository = CommentRepository(db)

    def create_comment(self, ticket_id: int, payload: dict) -> dict:
        return {}
