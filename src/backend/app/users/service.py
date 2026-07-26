from sqlalchemy.orm import Session

from app.users.repository import UserRepository


class UserService:
    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)

    def list_users(self) -> list:
        return []
