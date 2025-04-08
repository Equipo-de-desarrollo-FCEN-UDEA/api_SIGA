from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.application.user_application import UserApplication


class UserApplicationAcademicUnitBase(BaseModel):
    user_application_id: UUID
    academic_unit_id: UUID


class UserApplicationAcademicUnitCreate(UserApplicationAcademicUnitBase):
    pass


class UserApplicationAcademicUnitUpdate(BaseModel):
    user_application_id: UUID | None
    academic_unit_id: UUID | None


class UserApplicationAcademicUnitInDB(UserApplicationAcademicUnitBase):
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes = True


class UserApplicationAcademicUnit(BaseModel):
    academic_unit_id: UUID
    is_active: bool
    user_application: UserApplication
