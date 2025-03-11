from __future__ import annotations

from uuid import UUID

from app.errors.base import BaseErrors
from app.infraestructure.services.emails.application import create_application_email
from app.protocols.db.crud.application.user_application import (
    CRUDUserApplicationProtocol,
)
from app.protocols.db.models.application.user_application import UserApplication
from app.schemas.application.user_application import UserApplicationCreate
from app.schemas.application.user_application import UserApplicationUpdate
from app.services.base import ServiceBase

SERVICE_NOT_AVAILABLE = 'Service not available'


class UserApplicationService(
    ServiceBase[
        UserApplication,
        UserApplicationCreate,
        UserApplicationUpdate,
        CRUDUserApplicationProtocol,
    ],
):
    def create(
            self,
            *,
            obj_in: UserApplicationCreate,
            db,
            current_user_id: UUID | None = None,
    ) -> UserApplication:
        if self.observer is None:
            raise BaseErrors(code=503, detail=SERVICE_NOT_AVAILABLE)
        user_application = self.observer.create(
            obj_in=obj_in, db=db, current_user_id=current_user_id,
        )

        create_application_email.apply_async(
            args=[
                user_application.user.name,
                user_application.user.last_name,
                user_application.application.name,
                user_application.user.email,
            ],
        )
        return user_application


user_application_svc = UserApplicationService()
