from sqlalchemy.orm import Session

from app.users.repository import UserRepository
from app.users.schemas import UserOut


class UserService:
    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)

    def list_users(self) -> list[UserOut]:
        return [UserOut.model_validate(user) for user in self.repository.list_all()]
