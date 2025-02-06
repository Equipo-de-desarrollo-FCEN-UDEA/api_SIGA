from uuid import UUID
from app.services.base import ServiceBase
from app.schemas.application.user_application_academic_unit import UserApplicationAcademicUnitCreate, UserApplicationAcademicUnitUpdate
from app.protocols.db.models.application.user_application_academic_unit import UserApplicationAcademicUnit
from app.protocols.db.crud.application.user_application_academic_unit import CRUDUserApplicationAcademicUnitProtocol
from app.errors.base import BaseErrors

class UserApplicationAcademicUnitService(ServiceBase[UserApplicationAcademicUnit, UserApplicationAcademicUnitCreate, UserApplicationAcademicUnitUpdate, CRUDUserApplicationAcademicUnitProtocol]):
    
    def get_by_academic_unit(self,*, academic_unit_id: UUID, db) -> UserApplicationAcademicUnit:
        if self.observer is None:
            raise BaseErrors(code=503, detail="Service not available")
        return self.observer.get_by_academic_unit(academic_unit_id=academic_unit_id, db=db)

user_application_academic_unit_svc = UserApplicationAcademicUnitService()