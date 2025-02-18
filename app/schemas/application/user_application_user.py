from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.schemas.application.user_application import UserApplication
from app.schemas.utils.link_model import GeneralResponse


class UserApplicationUser(BaseModel):
    user_application_id: UUID
    user_id: UUID


class UserApplicationUserCreate(UserApplicationUser):
    pass


class UserApplicationUserUpdate(BaseModel):
    user_id: UUID | None
    is_active: bool | None


class UserApplicationUserPublic(GeneralResponse):
    user_application: UserApplication
    is_active: bool
