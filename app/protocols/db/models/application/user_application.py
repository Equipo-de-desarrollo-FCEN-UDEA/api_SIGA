from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.protocols.db.models.application.application import Application
from app.protocols.db.models.users.user import User
from app.protocols.db.utils.base_model import BaseModel


class UserApplicationStatus():
    name: str
    updated_by: str
    date: datetime


class UserApplication(BaseModel):
    user_id: UUID
    application_id: UUID

    user: User
    application: Application
