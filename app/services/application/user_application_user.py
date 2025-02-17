from __future__ import annotations

from app.protocols.db.crud.application.user_application_user import (
    CRUDUserApplicationUserProtocol,
)
from app.protocols.db.models.application.user_application_user import UserApplicationUser
from app.schemas.application.user_application_user import UserApplicationUserCreate
from app.schemas.application.user_application_user import UserApplicationUserUpdate
from app.services.base import ServiceBase


class UserApplicationUser(
    ServiceBase[
        UserApplicationUser,
        UserApplicationUserCreate,
        UserApplicationUserUpdate,
        CRUDUserApplicationUserProtocol,
    ],
):
    pass


user_application_user_svc = UserApplicationUser()
