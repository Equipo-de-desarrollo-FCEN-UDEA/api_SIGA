from __future__ import annotations

from abc import abstractmethod
from uuid import UUID

from sqlalchemy.orm import Session

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.application.user_application_academic_unit import (
    UserApplicationAcademicUnit,
)
from app.schemas.application.user_application import UserApplicationCreate
from app.schemas.application.user_application import UserApplicationUpdate


class CRUDUserApplicationAcademicUnitProtocol(
    CRUDProtocol[
        UserApplicationAcademicUnit,
        UserApplicationCreate,
        UserApplicationUpdate,
    ],
):
    @abstractmethod
    def get_by_academic_unit(
            self,
            *,
            academic_unit_id: UUID,
            db: Session,
    ) -> UserApplicationAcademicUnit:
        """
            This method is currently empty because the implementation details
            depend on the specific requirements of the application.
        """

    @abstractmethod
    def get_active(
            self,
            *,
            user_application_id: UUID,
            db: Session,
    ) -> UserApplicationAcademicUnit:
        """
            This method is currently empty because the implementation details
            depend on the specific requirements of the application.
        """
    @abstractmethod
    def get_by_user(
            self,
            *,
            user_id: UUID,
            db: Session,
    ) -> UserApplicationAcademicUnit:
        """
            This method is currently empty because the implementation details
            depend on the specific requirements of the application.
        """
    @abstractmethod
    def response(
            self,
            *,
            user_application_id: UUID,
            academic_unit_id: UUID,
            db: Session,
    ) -> UserApplicationAcademicUnit:
        """
            This method is currently empty because the implementation details
            depend on the specific requirements of the application.
        """
