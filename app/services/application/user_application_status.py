from __future__ import annotations

from app.protocols.db.crud.application.user_application_status import (
    CRUDUserApplicationStatusProtocol,
)
from app.protocols.db.models.application.user_application_status import (
    UserApplicationStatus,
)
from app.schemas.application.user_application_status import UserApplicationStatusCreate
from app.schemas.application.user_application_status import UserApplicationStatusUpdate
from app.services.base import ServiceBase


class UserApplicationStatusService(
    ServiceBase[
        UserApplicationStatus,
        UserApplicationStatusCreate,
        UserApplicationStatusUpdate,
        CRUDUserApplicationStatusProtocol,
    ],
):
    pass


user_application_status_svc = UserApplicationStatusService()
