from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.types import NonEmptyStr
from app.users.schemas import UserRef


class CommentCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: NonEmptyStr
    created_by: int = Field(alias="createdBy")


class CommentOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    message: str
    created_by: UserRef = Field(serialization_alias="createdBy")
    created_at: datetime = Field(serialization_alias="createdAt")
