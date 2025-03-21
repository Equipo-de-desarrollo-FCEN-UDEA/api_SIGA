from __future__ import annotations

from app.protocols.db.crud.application.status import CRUDStatusProtocol
from app.protocols.db.models.application.status import Status
from app.schemas.application.status import StatusCreate
from app.schemas.application.status import StatusUpdate
from app.services.base import ServiceBase


class StatusService(
    ServiceBase[
        Status,
        StatusCreate,
        StatusUpdate,
        CRUDStatusProtocol,
    ],
):
    pass


status_svc = StatusService()
