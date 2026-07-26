from sqlalchemy.orm import Session


class CommentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
