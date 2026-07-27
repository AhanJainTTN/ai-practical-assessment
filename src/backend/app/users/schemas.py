from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Role = Literal["requester", "agent"]


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: Role


class UserRef(BaseModel):
    """Embedded user reference on tickets/comments (no role)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
