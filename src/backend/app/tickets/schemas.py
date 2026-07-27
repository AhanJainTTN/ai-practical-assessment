from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.comments.schemas import CommentOut
from app.core.types import NonEmptyStr
from app.users.schemas import UserRef

Priority = Literal["Low", "Medium", "High"]
TicketStatus = Literal["Open", "In Progress", "Resolved", "Closed", "Cancelled"]


class TicketCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: NonEmptyStr
    description: NonEmptyStr
    priority: Priority
    created_by: int = Field(alias="createdBy")
    assigned_to: int | None = Field(default=None, alias="assignedTo")


class TicketUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: NonEmptyStr | None = None
    description: NonEmptyStr | None = None
    priority: Priority | None = None
    assigned_to: int | None = Field(default=None, alias="assignedTo")


class TicketTransition(BaseModel):
    status: TicketStatus


class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    priority: Priority
    status: TicketStatus
    assigned_to: UserRef | None = Field(serialization_alias="assignedTo")
    created_by: UserRef = Field(serialization_alias="createdBy")
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)


class TicketDetailOut(TicketOut):
    comments: list[CommentOut] = Field(default_factory=list)
