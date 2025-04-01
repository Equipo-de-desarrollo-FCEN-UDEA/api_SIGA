from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.constants import SERVICE_NOT_AVAILABLE
from app.errors.base import BaseErrors
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
    def get_next_step(self, current_step: int, application_id: str, db: Session) -> str:
        if self.observer is None:
            raise BaseErrors(code=503, detail=SERVICE_NOT_AVAILABLE)
        return self.observer.get_next_step(current_step, application_id, db)


application_status_svc = ApplicationStatusService()
