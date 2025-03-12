from __future__ import annotations

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.application.user_application import UserApplication
from app.schemas.application.user_application import UserApplicationCreate
from app.schemas.application.user_application import UserApplicationUpdate


class CRUDUserApplicationProtocol(
    CRUDProtocol[
        UserApplication,
        UserApplicationCreate, UserApplicationUpdate,
    ],
):
    def add_status(self, *, new_status, db_mongo, current_user):
        pass

    def create_user_application(
        self,
        *,
        obj_in,
        user_id,
        application_id,
        academic_unit_id,
        db_postgres,
        mongo_service,
        db_mongo,
    ):
        pass

    def upload_files(self, *, user_application_id, files, db, prefix):
        pass
