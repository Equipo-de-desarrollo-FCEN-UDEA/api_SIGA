from __future__ import annotations

from app.infraestructure.services.emails.application import create_application_email
from app.protocols.db.crud.application.user_application import CRUDUserApplicationProtocol
from app.protocols.db.models.application.user_application import UserApplication
from app.schemas.application.user_application import UserApplicationCreate
from app.schemas.application.user_application import UserApplicationUpdate
from app.services.base import ServiceBase


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
        user_application = super().create(obj_in=obj_in, db=db)
        create_application_email.apply_async(
            args=[
                user_application.user.name,
                user_application.user.last_name,
                user_application.application.name,
                user_application.user.email,
            ],
        )
        print('UserApplicationService -> create')
        return user_application


user_application_svc = UserApplicationService()
