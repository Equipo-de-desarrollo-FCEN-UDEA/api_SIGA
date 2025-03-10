from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class UserApplicationStatusBase(BaseModel):
    user_application_id: UUID
    status_id: UUID
    updated_by: UUID

    class Config:
        from_attributes = True


class UserApplicationStatusCreate(UserApplicationStatusBase):
    pass


class UserApplicationStatusUpdate(BaseModel):
    user_application_id: UUID | None
    status_id: UUID | None
    updated_by: UUID | None
