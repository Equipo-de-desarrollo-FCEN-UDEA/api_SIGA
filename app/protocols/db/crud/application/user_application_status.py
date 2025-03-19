from __future__ import annotations

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.application.user_application_status import (
    UserApplicationStatus,
)
from app.schemas.application.user_application_status import UserApplicationStatusCreate
from app.schemas.application.user_application_status import UserApplicationStatusUpdate


class CRUDUserApplicationStatusProtocol(
    CRUDProtocol
    [UserApplicationStatus, UserApplicationStatusCreate, UserApplicationStatusUpdate],
):
    pass
