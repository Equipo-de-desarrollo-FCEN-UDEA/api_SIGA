from __future__ import annotations

from uuid import UUID

from fastapi import UploadFile

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
    ) -> UserApplication:
        user_application: UserApplication = super().create(obj_in=obj_in, db=db)
        create_application_email.apply_async(
            args=[
                user_application.user.name,
                user_application.user.last_name,
                user_application.application.name,
                user_application.user.email,
            ],
        )
        return user_application

    def create_user_application(
            self,
            *,
            obj_in: UserApplicationCreate,
            current_user_id: UUID,
            application_id: UUID,
            academic_unit_id: UUID,
            db_postgres,
            mongo_service,
            db_mongo,
    ):
        if self.observer is None:
            raise BaseErrors(code=503, detail=SERVICE_NOT_AVAILABLE)
        return self.observer.create_user_application(
            obj_in=obj_in,
            user_id=current_user_id,
            application_id=application_id,
            academic_unit_id=academic_unit_id,
            db_postgres=db_postgres,
            mongo_service=mongo_service,
            db_mongo=db_mongo,
        )

    def upload_files(
            self,
            user_application_id: UUID,
            files: list[UploadFile],
            db,
            prefix: str | None = None,
    ) -> dict:
        if self.observer is None:
            raise BaseErrors(code=503, detail=SERVICE_NOT_AVAILABLE)
        return self.observer.upload_files(
            user_application_id=user_application_id,
            files=files,
            db=db,
            prefix=prefix,
        )


user_application_svc = UserApplicationService()
