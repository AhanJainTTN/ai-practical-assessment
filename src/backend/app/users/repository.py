from sqlalchemy.orm import Session

from app.users.models import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[User]:
        return self.db.query(User).order_by(User.id.asc()).all()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
