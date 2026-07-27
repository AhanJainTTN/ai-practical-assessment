from sqlalchemy.orm import Session, joinedload

from app.comments.models import Comment


class CommentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, comment: Comment) -> Comment:
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return (
            self.db.query(Comment)
            .options(joinedload(Comment.creator))
            .filter(Comment.id == comment.id)
            .one()
        )
