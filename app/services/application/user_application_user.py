from __future__ import annotations

from uuid import UUID

from app.errors.base import BaseErrors
from app.protocols.db.crud.application.user_application_user import (
    CRUDUserApplicationUserProtocol,
)
from app.protocols.db.models.application.user_application_user import UserApplicationUser
from app.schemas.application.user_application_user import UserApplicationUserCreate
from app.schemas.application.user_application_user import UserApplicationUserUpdate
from app.services.base import ServiceBase

NOT_AVAILABLE = 'Service not available'


class UserApplicationUser(
    ServiceBase[
        UserApplicationUser,
        UserApplicationUserCreate,
        UserApplicationUserUpdate,
        CRUDUserApplicationUserProtocol,
    ],
):

    def get_by_user(self, *, user_id: UUID, db) -> list[UserApplicationUser]:
        if self.observer is None:
            raise BaseErrors(
                code=503,
                detail=NOT_AVAILABLE,
            )
        return self.observer.get_by_user(
            user_id=user_id, db=db,
        )


user_application_user_svc = UserApplicationUser()
