from app.services.base import ServiceBase
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitCreate, UserRolAcademicUnitUpdate, UserRolAcademicUnitInDB
from app.protocols.db.models.users.user_rol_academic_unit import UserRolAcademicUnit
from app.protocols.db.models.organization.academic_unit import AcademicUnit
from app.protocols.db.crud.users.user_rol_academic_unit import CRUDUserRolAcademicUnitProtocol

from app.errors.base import BaseErrors
from uuid import UUID
from sqlalchemy.orm import Session

class UserRolAcademicUnitService(ServiceBase[UserRolAcademicUnit, UserRolAcademicUnitCreate, UserRolAcademicUnitUpdate, CRUDUserRolAcademicUnitProtocol]):
    def get_by_user_id(self, *, user_id: UUID, db: Session) -> UserRolAcademicUnit:
        if self.observer is None:
            raise BaseErrors(code=503, detail="Service not available")
        return self.observer.get_by_user_id(user_id=user_id, db=db)
    
    def get_student_committee(self, *, user_id:UUID, db:Session) -> UUID:
        return self.observer.get_student_committee(user_id=user_id, db=db)
    
    def get_academic_units_by_user_id_and_rol_id(self, *,user_id:UUID, rol_id: UUID, db: Session) -> list[AcademicUnit]:
        return self.observer.get_academic_units_by_user_id_and_rol_id(user_id=user_id, rol_id=rol_id, db=db)

user_rol_academic_unit_svc = UserRolAcademicUnitService()
