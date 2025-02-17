from __future__ import annotations

from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.application.user_application_user import (
    UserApplicationUser,
)
from app.schemas.application.user_application_user import UserApplicationUserCreate
from app.schemas.application.user_application_user import UserApplicationUserUpdate


class UserApplicationUserCrud(
    CRUDBase[
        UserApplicationUser,
        UserApplicationUserCreate,
        UserApplicationUserUpdate,
    ],
):
    pass


user_application_user_crud = UserApplicationUserCrud(UserApplicationUser)
