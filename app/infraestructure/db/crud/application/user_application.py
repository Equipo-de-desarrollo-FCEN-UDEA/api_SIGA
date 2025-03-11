from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.application.application import Application
from app.infraestructure.db.models.application.application_status import (
    ApplicationStatus,
)
from app.infraestructure.db.models.application.user_application import UserApplication
from app.schemas.application.user_application import UserApplicationCreate
from app.schemas.application.user_application import UserApplicationUpdate
from app.schemas.application.user_application_status import UserApplicationStatusCreate
from app.services.application.user_application_status import user_application_status_svc


class UserApplicationCrud(
    CRUDBase[
        UserApplication,
        UserApplicationCreate, UserApplicationUpdate,
    ],
):
    def create(
        self,
        *, obj_in: UserApplicationCreate, db: Session, current_user_id: UUID,
    ) -> UserApplication:
        user_application = super().create(obj_in=obj_in, db=db)
        application: Application = user_application.application
        user_application_id = user_application.id
        current_user_id = current_user_id
        first_application_status: ApplicationStatus = application.application_status[0]
        first_application_status_id = first_application_status.status_id

        user_application_status = UserApplicationStatusCreate(
            user_application_id=user_application_id,
            status_id=first_application_status_id,
            updated_by=current_user_id,
        )

        user_application_status_svc.create(obj_in=user_application_status, db=db)

        return user_application


user_application_crud = UserApplicationCrud(UserApplication)
