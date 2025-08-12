from __future__ import annotations

from abc import abstractmethod
from uuid import UUID

from sqlalchemy.orm import Session

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.organization.academic_unit import AcademicUnit
from app.protocols.db.models.users.user_rol_academic_unit import UserRolAcademicUnit
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitCreate
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitUpdate


class CRUDUserRolAcademicUnitProtocol(
    CRUDProtocol[
        UserRolAcademicUnit,
        UserRolAcademicUnitCreate, UserRolAcademicUnitUpdate,
    ],
):
    @abstractmethod
    def get_by_user_id(self, *, user_id: UUID, db: Session) -> UserRolAcademicUnit:
        pass

    @abstractmethod
    def get_student_committee(self, *, user_id: UUID, db: Session) -> UUID:
        pass

    @abstractmethod
    def get_professor_institute_council(self, *, user_id: UUID, db: Session) -> UUID:
        pass

    @abstractmethod
    def get_professor_faculty_council(self, *, user_id: UUID, db: Session) -> UUID:
        pass

    @abstractmethod
    def get_center(self, *, user_id: UUID, db: Session) -> list[UUID]:
        pass

    @abstractmethod
    def get_academic_units_by_user_id_and_rol_id(
        self,
        *, user_id: UUID, rol_id: UUID, db: Session,
    ) -> list[AcademicUnit]:
        pass

    @abstractmethod
    def get_by_academic_unit_id(
        self,
        *, academic_unit_id: UUID, rol_name: str | None = None, db: Session,
    ) -> list[UserRolAcademicUnit]:
        pass
