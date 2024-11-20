from uuid import UUID
from sqlalchemy.orm import Session
from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.users.user_rol_academic_unit import UserRolAcademicUnit
from app.protocols.db.models.organization.academic_unit import AcademicUnit
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitCreate, UserRolAcademicUnitUpdate

class CRUDUserRolAcademicUnitProtocol(CRUDProtocol[UserRolAcademicUnit, UserRolAcademicUnitCreate, UserRolAcademicUnitUpdate]):
    def get_by_user_id(self, *, user_id: UUID, db: Session) -> UserRolAcademicUnit:
        pass
    
    def get_student_committee(self, *, user_id:UUID, db: Session) -> UUID:
        pass

    def get_academic_units_by_user_id_and_rol_id(self, *,user_id:UUID, rol_id: UUID, db: Session) -> list[AcademicUnit]:
        pass