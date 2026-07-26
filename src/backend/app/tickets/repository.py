from sqlalchemy.orm import Session


class TicketRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
