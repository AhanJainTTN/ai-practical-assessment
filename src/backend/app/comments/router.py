from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.comments.service import CommentService

router = APIRouter(prefix="/tickets", tags=["comments"])


@router.post("/{ticket_id}/comments", status_code=201)
def create_comment(
    ticket_id: int,
    payload: dict,
    db: Session = Depends(get_db),
) -> dict:
    return CommentService(db).create_comment(ticket_id, payload)
