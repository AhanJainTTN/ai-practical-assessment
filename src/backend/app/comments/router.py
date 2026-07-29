from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.comments.schemas import CommentCreate, CommentOut
from app.comments.service import CommentService
from app.core.database import get_db

router = APIRouter(prefix="/tickets", tags=["comments"])


@router.post("/{ticket_id}/comments", response_model=CommentOut, status_code=201)
def create_comment(
    ticket_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
) -> CommentOut:
    return CommentService(db).create_comment(ticket_id, payload)
