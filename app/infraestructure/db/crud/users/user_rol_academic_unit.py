from __future__ import annotations

from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.organization.academic_unit import AcademicUnit
from app.infraestructure.db.models.user.rol import Rol
from app.infraestructure.db.models.user.user_rol_academic_unit import UserRolAcademicUnit
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitCreate
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitUpdate


class UserRolAcademicUnitCrud(
    CRUDBase[UserRolAcademicUnit, UserRolAcademicUnitCreate, UserRolAcademicUnitUpdate],
):
    def get_by_user_id(self, *, user_id: UUID, db: Session) -> UserRolAcademicUnit:
        return db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.rol),
            joinedload(UserRolAcademicUnit.academic_unit),
        ).filter(self.model.user_id == user_id).all()

    def get_student_committee(self, *, user_id: UUID, db: Session) -> UUID:
        # UUIDs constantes
        ESTUDIANTE_PREGRADO_ROL_ID = UUID('939875b2-3e34-4a17-9f3c-76cabba73f52')
        ESTUDIANTE_POSGRADO_ROL_ID = UUID('1ca355db-8700-4ee7-883b-18b8bbed403b')
        TYPE_COMITE = UUID('d1085905-eed1-4e3c-bae6-9f3b17295eca')

        # Realizamos una sola consulta para ambos roles
        user_rol = db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.academic_unit).joinedload(
                AcademicUnit.academic_unit,
            ).joinedload(AcademicUnit.academic_units),
        ).filter(
            (self.model.user_id == user_id) &
            (
                (self.model.rol_id == ESTUDIANTE_PREGRADO_ROL_ID) |
                (self.model.rol_id == ESTUDIANTE_POSGRADO_ROL_ID)
            ) & (self.model.is_active),
        ).first()

        # Lista de unidades académicas "hijas" del instituto, como los comités
        lista = user_rol.academic_unit.academic_units
        for academic_unit in lista:
            if (
                (
                    user_rol.rol_id == ESTUDIANTE_PREGRADO_ROL_ID and
                    academic_unit.academic_unit_type_id == TYPE_COMITE
                ) or
                (
                    user_rol.rol_id == ESTUDIANTE_POSGRADO_ROL_ID and
                    academic_unit.academic_unit_type_id == TYPE_COMITE
                )
            ):
                return academic_unit.id

        raise HTTPException(404, 'No se encontró el comité del estudiante')

    def get_professor_council(self, *, user_id: UUID, db: Session) -> UUID:
        # UUIDs constantes
        PROFESOR_ROL_ID = UUID('0c1875e9-50b8-4590-80d1-6afce3ea152b')
        TYPE_CONSEJO_INSTITUTO = UUID('c4e1c617-9308-4d38-bc13-ae8db0858f31')

        # Consulta el rol del profesor con las relaciones necesarias
        user_rol = db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.academic_unit).joinedload(
                AcademicUnit.academic_unit,
            ).joinedload(AcademicUnit.academic_units),
        ).filter(
            self.model.user_id == user_id,
            self.model.rol_id == PROFESOR_ROL_ID,
            self.model.is_active,
        ).first()

        if not user_rol:
            raise HTTPException(404, 'No se encontró el rol del profesor')

        # Lista de unidades académicas "hijas" del instituto
        lista = user_rol.academic_unit.academic_units

        for academic_unit in lista:
            print('===================================', academic_unit.name)
            if academic_unit.academic_unit_type_id == TYPE_CONSEJO_INSTITUTO:
                return academic_unit.id

        raise HTTPException(404, 'No se encontró el comité profesoral del usuario')

    def get_academic_units_by_user_id_and_rol_id(
            self,
            *,
            user_id: UUID,
            rol_id: UUID,
            db: Session,
    ) -> list[AcademicUnit]:
        user_rol_academic_units = db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.academic_unit),
        ).filter((self.model.user_id == user_id) & (self.model.rol_id == rol_id)).all()

        return [
            user_rol_academic_unit.academic_unit
            for user_rol_academic_unit in user_rol_academic_units
        ]

    def get_by_academic_unit_id(
            self,
            *,
            academic_unit_id: UUID,
            rol_name: str | None = None,
            db: Session,
    ) -> UserRolAcademicUnit:

        query = (
            db.query(UserRolAcademicUnit)
            .join(Rol)  # Hace explícito el JOIN con la tabla Rol
            .filter(UserRolAcademicUnit.academic_unit_id == academic_unit_id)
        )

        if rol_name:
            query = query.filter(Rol.name == rol_name)

        return query.all()


user_rol_academic_unit_crud = UserRolAcademicUnitCrud(UserRolAcademicUnit)
