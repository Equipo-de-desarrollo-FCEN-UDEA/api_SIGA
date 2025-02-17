from __future__ import annotations

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.application.user_application_user import UserApplicationUser
from app.schemas.application.user_application_user import UserApplicationUserCreate
from app.schemas.application.user_application_user import UserApplicationUserUpdate


class CRUDUserApplicationUserProtocol(
    CRUDProtocol[
        UserApplicationUser,
        UserApplicationUserCreate,
        UserApplicationUserUpdate,
    ],
):
    pass
