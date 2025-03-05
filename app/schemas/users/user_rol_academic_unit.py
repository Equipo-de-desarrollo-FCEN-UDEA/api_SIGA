from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.schemas.organization.academic_unit import AcademicUnit
from app.schemas.users.rol import Rol
from app.schemas.utils.link_model import GeneralResponse


class UserRolAcademicUnitBase(BaseModel):
    rol_id: UUID
    user_id: UUID
    academic_unit_id: UUID
    is_active: bool | None = True


class UserRolAcademicUnitCreate(UserRolAcademicUnitBase):
    ...


class UserRolAcademicUnitUpdate(BaseModel):
    ...


class UserRolAcademicUnitInDB(GeneralResponse, UserRolAcademicUnitBase):
    ...


class UserRolAcademicUnit(BaseModel):
    rol: Rol
    academic_unit: AcademicUnit

    class Config:
        orm_mode = True
        from_attributes = True


class UserPublic(BaseModel):
    name: str
    last_name: str

    class Config:
        from_attributes = True


class UserRolAcademicUnitPublic(BaseModel):
    user: UserPublic
    rol: Rol
    academic_unit: AcademicUnit

    class Config:
        from_attributes = True
