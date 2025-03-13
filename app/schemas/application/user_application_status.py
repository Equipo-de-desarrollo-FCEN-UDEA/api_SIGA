from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.application.status import StatusPublic
from app.schemas.users.user import UserPublic


class UserApplicationStatusBase(BaseModel):
    user_application_id: UUID
    status_id: UUID
    updated_by: UUID

    class Config:
        from_attributes = True


class UserApplicationStatusCreate(UserApplicationStatusBase):
    observation: str | None = None


class UserApplicationStatusUpdate(BaseModel):
    user_application_id: UUID | None
    status_id: UUID | None
    updated_by: UUID | None


class UserApplicationStatusPublic(BaseModel):
    status: StatusPublic
    user: UserPublic
    observation: str | None
    created_at: datetime

    class Config:
        from_attributes = True
