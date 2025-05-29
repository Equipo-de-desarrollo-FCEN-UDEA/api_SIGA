from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.errors.base import BaseErrors
from app.protocols.db.crud.users.user_rol_academic_unit import (
    CRUDUserRolAcademicUnitProtocol,
)
from app.protocols.db.models.organization.academic_unit import AcademicUnit
from app.protocols.db.models.users.user_rol_academic_unit import UserRolAcademicUnit
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitCreate
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitUpdate
from app.services.base import ServiceBase

SERVICE_NOT_AVAILABLE = 'Service not available'


class UserRolAcademicUnitService(
    ServiceBase[
        UserRolAcademicUnit,
        UserRolAcademicUnitCreate,
        UserRolAcademicUnitUpdate,
        CRUDUserRolAcademicUnitProtocol,
    ],
):
    def get_by_user_id(self, *, user_id: UUID, db: Session) -> UserRolAcademicUnit:
        if self.observer is None:
            raise BaseErrors(code=503, detail=SERVICE_NOT_AVAILABLE)
        return self.observer.get_by_user_id(user_id=user_id, db=db)

    def get_student_committee(self, *, user_id: UUID, db: Session) -> UUID:
        if self.observer is None:
            raise BaseErrors(code=503, detail=SERVICE_NOT_AVAILABLE)
        return self.observer.get_student_committee(user_id=user_id, db=db)

    def get_professor_council(self, *, user_id: UUID, db: Session) -> UUID:
        if self.observer is None:
            raise BaseErrors(code=503, detail=SERVICE_NOT_AVAILABLE)
        return self.observer.get_professor_council(user_id=user_id, db=db)

    def get_academic_units_by_user_id_and_rol_id(
        self,
        *, user_id: UUID, rol_id: UUID, db: Session,
    ) -> list[AcademicUnit]:
        if self.observer is None:
            raise BaseErrors(code=503, detail=SERVICE_NOT_AVAILABLE)
        return self.observer.get_academic_units_by_user_id_and_rol_id(
            user_id=user_id,
            rol_id=rol_id, db=db,
        )

    def get_by_academic_unit_id(
        self,
        *, academic_unit_id: UUID, rol_name: str | None = None, db: Session,
    ) -> list[UserRolAcademicUnit]:
        if self.observer is None:
            raise BaseErrors(code=503, detail=SERVICE_NOT_AVAILABLE)
        return self.observer.get_by_academic_unit_id(
            academic_unit_id=academic_unit_id,
            rol_name=rol_name, db=db,
        )


user_rol_academic_unit_svc = UserRolAcademicUnitService()
