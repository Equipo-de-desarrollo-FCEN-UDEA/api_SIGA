from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.organization.academic_unit import AcademicUnit
from app.infraestructure.db.models.organization.academic_unit_type import AcademicUnitType
from app.schemas.organization.academic_unit import AcademicUnitCreate, AcademicUnitUpdate

from sqlalchemy.orm import Session, joinedload
from uuid import UUID


class AcademicUnitCrud(CRUDBase[AcademicUnit, AcademicUnitCreate, AcademicUnitUpdate]):
    def get(self, *, id: UUID, db: Session) -> AcademicUnit:
        with db:
            return db.query(AcademicUnit).options(
                joinedload(AcademicUnit.academic_units),
                joinedload(AcademicUnit.academic_units).joinedload(AcademicUnit.academic_units)
            ).get(id)


academic_unit_crud = AcademicUnitCrud(AcademicUnit)