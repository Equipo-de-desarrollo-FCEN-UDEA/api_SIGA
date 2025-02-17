from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class UserApplicationUser(BaseModel):
    user_application_id: UUID
    user_id: UUID
    is_active: bool = True


class UserApplicationUserCreate(UserApplicationUser):
    pass


class UserApplicationUserUpdate(BaseModel):
    user_id: UUID | None
    is_active: bool | None
