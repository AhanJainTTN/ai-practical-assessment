from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.tickets.schemas import (
    TicketCreate,
    TicketDetailOut,
    TicketOut,
    TicketTransition,
    TicketUpdate,
)
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


@router.get("", response_model=list[TicketOut])
def list_tickets(
    status: str | None = None,
    db: Session = Depends(get_db),
) -> list[TicketOut]:
    return TicketService(db).list_tickets(status=status)


@router.post("", response_model=TicketOut, status_code=201)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)) -> TicketOut:
    return TicketService(db).create_ticket(payload)


@router.get("/{ticket_id}", response_model=TicketDetailOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)) -> TicketDetailOut:
    return TicketService(db).get_ticket(ticket_id)


@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    db: Session = Depends(get_db),
) -> TicketOut:
    return TicketService(db).update_ticket(ticket_id, payload)


@router.post("/{ticket_id}/transitions", response_model=TicketOut)
def transition_ticket(
    ticket_id: int,
    payload: TicketTransition,
    db: Session = Depends(get_db),
) -> TicketOut:
    return TicketService(db).transition_ticket(ticket_id, payload.status)
