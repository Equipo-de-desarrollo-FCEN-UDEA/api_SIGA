from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ORMError
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
    def get_by_user(self, *, user_id: UUID, db: Session) -> list[UserApplicationUser]:
        with db:
            response = db.query(UserApplicationUser).filter(
                self.model.user_id == user_id,
            ).all()
        if not response:
            raise ORMError(
                f'No user application user found with user {user_id}',
            )
        return response


user_application_user_crud = UserApplicationUserCrud(UserApplicationUser)
