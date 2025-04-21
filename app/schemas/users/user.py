from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from app.infraestructure.db.models.user.user import IdentificationType
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnit
from app.schemas.utils.base_model import GeneralResponse


class UserBase(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    identification_type: IdentificationType
    identification_number: str
    phone: str | None
    is_active: bool = False


class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: str | None = None
    name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
    phone: str | None = None
    hashed_password: str | None = None
    identification_type: IdentificationType | None = None
    identification_number: str | None = None

    class Config:
        from_attributes = True


class UserCreateInDB(UserBase):
    hashed_password: str

    class Config:
        from_attributes = True


class UserUpdateInDB(UserBase):
    id: UUID | None = None
    hashed_password: str

    class Config:
        from_attributes = True


class UserInDB(GeneralResponse, UserBase):
    ...


class UserSearch(BaseModel):
    names__icontains: str | None = Field(None, alias='names')
    email__icontains: str | None = Field(None, alias='email')

    class Config:
        populate_by_name = True


class User(UserBase):
    id: UUID
    user_roles_academic_units: list[UserRolAcademicUnit]

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    id: UUID | None = None
    name: str
    last_name: str

    class Config:
        from_attributes = True


class UserSession(UserPublic):
    scopes: list[str]
