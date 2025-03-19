from __future__ import annotations

from app.protocols.db.crud.application.application_status import (
    CRUDApplicationStatusProtocol,
)
from app.protocols.db.models.application.application_status import ApplicationStatus
from app.schemas.application.application_status import ApplicationStatusCreate
from app.schemas.application.application_status import ApplicationStatusUpdate
from app.services.base import ServiceBase


class ApplicationStatusService(
    ServiceBase[
        ApplicationStatus,
        ApplicationStatusCreate,
        ApplicationStatusUpdate,
        CRUDApplicationStatusProtocol,
    ],
):
    pass


application_status_svc = ApplicationStatusService()
