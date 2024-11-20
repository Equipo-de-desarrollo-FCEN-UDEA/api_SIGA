from fastapi.exceptions import HTTPException 
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.user.user_rol_academic_unit import UserRolAcademicUnit
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitCreate, UserRolAcademicUnitUpdate

from app.infraestructure.db.models.organization.academic_unit import AcademicUnit

class UserRolAcademicUnitCrud(CRUDBase[UserRolAcademicUnit, UserRolAcademicUnitCreate, UserRolAcademicUnitUpdate]):
    def get_by_user_id(self, *, user_id: UUID, db: Session) -> UserRolAcademicUnit:
        return db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.rol),
            joinedload(UserRolAcademicUnit.academic_unit)
        ).filter(self.model.user_id == user_id).all()
    
    def get_student_committee(self, *, user_id: UUID, db: Session) -> UUID:
        # UUIDs constantes
        ESTUDIANTE_PREGRADO_ROL_ID = UUID('939875b2-3e34-4a17-9f3c-76cabba73f52')
        ESTUDIANTE_POSGRADO_ROL_ID = UUID('1ca355db-8700-4ee7-883b-18b8bbed403b')
        TYPE_COMITE_PREGRADO = UUID('f44c11ab-46f9-49e2-b98c-c1e139dc7c58')
        TYPE_COMITE_POSGRADO = UUID('340e13c3-1dbe-47a0-b735-d72853c5ea78')

        # Realizamos una sola consulta para ambos roles
        user_rol = db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.academic_unit).joinedload(AcademicUnit.academic_unit).joinedload(AcademicUnit.academic_units)
        ).filter(
            (self.model.user_id == user_id) & 
            (
                (self.model.rol_id == ESTUDIANTE_PREGRADO_ROL_ID) |
                (self.model.rol_id == ESTUDIANTE_POSGRADO_ROL_ID)
            ) & (self.model.is_active == True)
        ).first()

        # Procesamos los resultados
        lista = user_rol.academic_unit.academic_unit.academic_units #devuelve el listado de unidades academicas que pertenecen al instituto del cual hace parte el programa academico del estudiante de un estudiante
        for academic_unit in lista:
            if (
                (user_rol.rol_id == ESTUDIANTE_PREGRADO_ROL_ID and academic_unit.academic_unit_type_id == TYPE_COMITE_PREGRADO) or
                (user_rol.rol_id == ESTUDIANTE_POSGRADO_ROL_ID and academic_unit.academic_unit_type_id == TYPE_COMITE_POSGRADO)
            ):
                return academic_unit.id

        raise HTTPException(404, "No se encontró el comité del estudiante")
    
    def get_academic_units_by_user_id_and_rol_id(self, *,user_id: UUID, rol_id: UUID, db: Session) -> list[AcademicUnit]:
        user_rol_academic_units = db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.academic_unit)
        ).filter((self.model.user_id == user_id)&(self.model.rol_id == rol_id)).all()

        return [user_rol_academic_unit.academic_unit for user_rol_academic_unit in user_rol_academic_units]
    
user_rol_academic_unit_crud = UserRolAcademicUnitCrud(UserRolAcademicUnit)