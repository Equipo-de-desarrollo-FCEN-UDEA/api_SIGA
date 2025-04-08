from __future__ import annotations

from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.application.user_application_status import (
    UserApplicationStatus,
)
from app.schemas.application.user_application_status import UserApplicationStatusCreate
from app.schemas.application.user_application_status import UserApplicationStatusUpdate


class UserApplicationStatusCrud(
    CRUDBase[
        UserApplicationStatus,
        UserApplicationStatusCreate,
        UserApplicationStatusUpdate,
    ],
):
    pass


user_application_status_crud = UserApplicationStatusCrud(UserApplicationStatus)
