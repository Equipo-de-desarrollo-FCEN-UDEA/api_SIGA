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
    
    def response(self,*, user_application_id: UUID, academic_unit_id: UUID, db: Session) -> UserApplicationAcademicUnit:
        with db:
            user_application_academic_unit = db.query(UserApplicationAcademicUnit).filter(
                self.model.user_application_id ==  user_application_id,
                self.model.academic_unit_id == academic_unit_id, 
                ).first()
            if not user_application_academic_unit:
                raise ORMError(f"No user application academic unit found with user application {user_application_id} and academic unit {academic_unit_id}")
            user_application_academic_unit.is_active = False
            db.commit()
            db.refresh(user_application_academic_unit)
        return user_application_academic_unit

user_application_academic_unit_crud = UserApplicationAcademicUnitCrud(UserApplicationAcademicUnit)