from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from app.schemas.utils.base_model import GeneralResponse

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