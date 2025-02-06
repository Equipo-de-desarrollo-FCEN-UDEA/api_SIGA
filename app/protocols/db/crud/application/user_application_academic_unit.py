from uuid import UUID

from sqlalchemy.orm import Session
from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.application.user_application_academic_unit import UserApplicationAcademicUnit
from app.schemas.application.user_application import UserApplicationCreate, UserApplicationUpdate

class CRUDUserApplicationAcademicUnitProtocol(CRUDProtocol[UserApplicationAcademicUnit, UserApplicationCreate, UserApplicationUpdate]):
    def get_by_academic_unit(self,*, academic_unit_id: UUID, db: Session) -> UserApplicationAcademicUnit:
        ...