from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

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
    def get_by_user(self, *, user_id: UUID, db: Session) -> list[UserApplicationUser]:
        """
            This method is currently empty because the implementation details
            depend on the specific requirements of the application.
        """
