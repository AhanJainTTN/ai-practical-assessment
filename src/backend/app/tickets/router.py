from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.tickets.service import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/export.csv")
def export_tickets(
    created_by: int = Query(..., alias="createdBy"),
    db: Session = Depends(get_db),
) -> Response:
    csv_content = TicketService(db).export_csv(created_by)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tickets-export.csv"},
    )


@router.get("")
def list_tickets(
    status: str | None = None,
    db: Session = Depends(get_db),
) -> list:
    return TicketService(db).list_tickets(status=status)


@router.post("", status_code=201)
def create_ticket(payload: dict, db: Session = Depends(get_db)) -> dict:
    TicketService(db).create_ticket(payload)
    return {}


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)) -> dict:
    TicketService(db).get_ticket(ticket_id)
    return {}


@router.patch("/{ticket_id}")
def update_ticket(
    ticket_id: int,
    payload: dict,
    db: Session = Depends(get_db),
) -> dict:
    TicketService(db).update_ticket(ticket_id, payload)
    return {}


@router.post("/{ticket_id}/transitions")
def transition_ticket(
    ticket_id: int,
    payload: dict,
    db: Session = Depends(get_db),
) -> dict:
    status = payload.get("status", "")
    TicketService(db).transition_ticket(ticket_id, status)
    return {}
