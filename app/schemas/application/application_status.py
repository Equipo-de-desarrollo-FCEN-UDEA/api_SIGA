from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class ApplicationStatusBase(BaseModel):
    application_id: UUID
    status_id: UUID
    step: int

    class Config:
        from_attributes = True


class ApplicationStatusCreate(ApplicationStatusBase):
    pass


class ApplicationStatusUpdate(BaseModel):
    application_id: UUID | None
    status_id: UUID | None
    step: int | None
