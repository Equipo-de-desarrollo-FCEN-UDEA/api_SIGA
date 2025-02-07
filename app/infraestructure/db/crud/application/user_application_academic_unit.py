from uuid import UUID
from app.core.exceptions import ORMError

from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.application.user_application_academic_unit import UserApplicationAcademicUnit
from app.schemas.application.user_application_academic_unit import UserApplicationAcademicUnitCreate, UserApplicationAcademicUnitUpdate

from sqlalchemy.orm import Session

class UserApplicationAcademicUnitCrud(CRUDBase[UserApplicationAcademicUnit, UserApplicationAcademicUnitCreate, UserApplicationAcademicUnitUpdate]):
    def get_by_academic_unit(self,*, academic_unit_id: UUID, db: Session) -> UserApplicationAcademicUnit:
        with db:
            response =  db.query(UserApplicationAcademicUnit).filter(self.model.academic_unit_id == academic_unit_id).all()
        if not response:
            raise ORMError(f"No user application academic unit found with academic unit {academic_unit_id}")
        return response

user_application_academic_unit_crud = UserApplicationAcademicUnitCrud(UserApplicationAcademicUnit)