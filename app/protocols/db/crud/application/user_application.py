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
        """
        Add a new status to the user application
        """

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
        """
        Create a new user application with your mongo schema
        """

    def upload_files(self, *, user_application_id, files, db, prefix):
        """
        upload user application files
        """

    def get_by_academic_unit(self, *, academic_unit_id, db):
        """
        Get all user applications sent to a unit academic
        """

    def get_to_user(self, *, user_id, db):
        """
        Get all user applications sent to a user
        """

    def get_by_user_id(self, *, user_id, db):
        """
        Get all user applications sent to a user
        """
