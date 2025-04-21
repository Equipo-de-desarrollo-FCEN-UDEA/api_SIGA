from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.application.application import Application
from app.schemas.application.application import ApplicationPublic
from app.schemas.application.user_application_status import (
    UserApplicationStatusPublic,
)
from app.schemas.organization.academic_unit import AcademicUnit
from app.schemas.users.user import UserInDB
from app.schemas.users.user import UserPublic
from app.schemas.utils.base_model import GeneralResponse


class UserApplicationStatus(BaseModel):
    name: str
    updated_by: UUID
    date: datetime


class UserApplicationBase(BaseModel):
    user_id: UUID
    application_id: UUID


class UserApplicationCreate(UserApplicationBase):
    pass


class UserApplicationUpdate(BaseModel):
    user_id: UUID | None
    application_id: UUID | None


class UserApplicationCreateInDB(GeneralResponse, UserApplicationBase):
    pass


class UserApplicationInfo(GeneralResponse, UserApplicationBase):
    application: Application
    user: UserInDB


class UserApplication(BaseModel):
    id: UUID
    application: Application
    user: UserInDB

    class Config:
        from_attributes = True


class UserApplicationAcademicUnitPublic(BaseModel):
    is_active: bool
    academic_unit: AcademicUnit | None = None

    class Config:
        from_attributes = True


class UserApplicationPublic(BaseModel):
    id: UUID
    consecutive: int
    user: UserPublic
    application: ApplicationPublic
    user_application_academic_units: list[UserApplicationAcademicUnitPublic]
    user_application_status: list[UserApplicationStatusPublic]
    documents: list[dict] | None = None
    info: dict | None = None

    class Config:
        from_attributes = True
