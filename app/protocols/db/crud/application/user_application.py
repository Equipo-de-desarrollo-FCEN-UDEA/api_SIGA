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

    def create(self, *, obj_in, db, current_user_id):
        pass
