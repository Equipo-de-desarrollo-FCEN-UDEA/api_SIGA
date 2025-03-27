from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class ApplicationBase(BaseModel):
    name: str
    description: str
    academic_unit_id: UUID

    class config:
        from_attributes = True


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    name: str | None
    description: str | None
    academic_unit_id: UUID | None


class Application(ApplicationBase):
    id: UUID

    class Config:
        from_attributes = True


class ApplicationPublic(BaseModel):
    id: UUID
    name: str
    description: str

    class Config:
        from_attributes = True
