from sqlalchemy.orm import Session

from app.tickets.repository import TicketRepository


class TicketService:
    def __init__(self, db: Session) -> None:
        self.repository = TicketRepository(db)

    def list_tickets(self, status: str | None = None) -> list:
        return []

    def get_ticket(self, ticket_id: int) -> None:
        return None

    def create_ticket(self, payload: dict) -> None:
        return None

    def update_ticket(self, ticket_id: int, payload: dict) -> None:
        return None

    def transition_ticket(self, ticket_id: int, status: str) -> None:
        return None

    def export_csv(self, created_by: int) -> str:
        return (
            "id,title,description,priority,status,assigneeName,assigneeEmail,"
            "creatorName,creatorEmail,createdAt,updatedAt,commentCount,comments\n"
        )
