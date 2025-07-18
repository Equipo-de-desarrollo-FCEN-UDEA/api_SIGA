from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.organization.academic_unit import AcademicUnit
from app.schemas.organization.academic_unit import AcademicUnitCreate
from app.schemas.organization.academic_unit import AcademicUnitUpdate


class AcademicUnitCrud(
    CRUDBase[
        AcademicUnit,
        AcademicUnitCreate,
        AcademicUnitUpdate,
    ],
):
    def get(self, *, id: UUID, db: Session) -> AcademicUnit:
        with db:
            return db.query(AcademicUnit).options(
                joinedload(AcademicUnit.academic_units),
                joinedload(AcademicUnit.academic_units).joinedload(
                    AcademicUnit.academic_units,
                ),
            ).get(id)


academic_unit_crud = AcademicUnitCrud(AcademicUnit)
