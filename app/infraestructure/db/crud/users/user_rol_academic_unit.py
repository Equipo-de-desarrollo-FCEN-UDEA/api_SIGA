from __future__ import annotations

from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.core.constants import ESTUDIANTE_POSGRADO_ROL_ID
from app.core.constants import ESTUDIANTE_PREGRADO_ROL_ID
from app.core.constants import PROFESOR_ROL_ID
from app.core.constants import TYPE_COMITE
from app.core.constants import TYPE_COMITE_POSGRADO
from app.core.constants import TYPE_COMITE_PREGRADO
from app.core.constants import TYPE_CONSEJO
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

        # Realizamos una sola consulta para ambos roles
        user_rol = db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.academic_unit).joinedload(
                AcademicUnit.academic_unit,
            ).joinedload(AcademicUnit.academic_units),
        ).filter(
            (self.model.user_id == user_id) &
            (
                (self.model.rol_id == UUID(ESTUDIANTE_PREGRADO_ROL_ID)) |
                (self.model.rol_id == UUID(ESTUDIANTE_POSGRADO_ROL_ID))
            ) & (self.model.is_active),
        ).first()

        # Lista de unidades académicas "hijas" del instituto, como los comités
        lista = user_rol.academic_unit.academic_units
        for academic_unit in lista:

            # Si la facultad solo tiene comité
            if (
                (
                    user_rol.rol_id == UUID(ESTUDIANTE_PREGRADO_ROL_ID) or
                    user_rol.rol_id == UUID(ESTUDIANTE_POSGRADO_ROL_ID)
                ) and
                academic_unit.academic_unit_type_id == UUID(TYPE_COMITE)
            ):
                return academic_unit.id

            # Si la facultad tiene comité de pregrado y/o posgrado
            if (
                user_rol.rol_id == UUID(ESTUDIANTE_PREGRADO_ROL_ID) and
                academic_unit.academic_unit_type_id == UUID(TYPE_COMITE_PREGRADO)
            ):
                return academic_unit.id
            if (
                user_rol.rol_id == UUID(ESTUDIANTE_POSGRADO_ROL_ID) and
                academic_unit.academic_unit_type_id == UUID(TYPE_COMITE_POSGRADO)
            ):
                return academic_unit.id

        raise HTTPException(404, 'No se encontró el comité del estudiante')

    def get_professor_institute_council(self, *, user_id: UUID, db: Session) -> UUID:

        # Consulta el rol del profesor con las relaciones necesarias
        user_rol = db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.academic_unit).joinedload(
                AcademicUnit.academic_unit,
            ).joinedload(AcademicUnit.academic_units),
        ).filter(
            self.model.user_id == user_id,
            self.model.rol_id == UUID(PROFESOR_ROL_ID),
            self.model.is_active,
        ).first()

        if not user_rol:
            raise HTTPException(404, 'No se encontró el rol del profesor')

        # Lista de unidades académicas "hijas" del instituto, como los consejos
        # o comités
        lista = user_rol.academic_unit.academic_units
        for academic_unit in lista:
            # Si la facultad tiene consejos de instituto
            if academic_unit.academic_unit_type_id == UUID(TYPE_CONSEJO):
                return academic_unit.id

            # Si la facultad tiene comités de departamento
            if academic_unit.academic_unit_type_id == UUID(TYPE_COMITE):
                return academic_unit.id

        raise HTTPException(404, 'No se encontró el comité profesoral del usuario')

    def get_professor_faculty_council(self, *, user_id: UUID, db: Session) -> UUID:

        # Consulta el rol del profesor con las relaciones necesarias
        user_rol = db.query(UserRolAcademicUnit).options(
            joinedload(UserRolAcademicUnit.academic_unit).joinedload(
                AcademicUnit.academic_unit,
            ).joinedload(AcademicUnit.academic_units),
        ).filter(
            self.model.user_id == user_id,
            self.model.rol_id == UUID(PROFESOR_ROL_ID),
            self.model.is_active,
        ).first()

        if not user_rol:
            raise HTTPException(404, 'No se encontró el rol del profesor')

        # Lista de unidades académicas "hijas" del instituto, como los consejos
        # o comités
        lista = user_rol.academic_unit.academic_unit.academic_units
        for academic_unit in lista:
            # Si la facultad tiene consejo de facultad
            if academic_unit.academic_unit_type_id == UUID(TYPE_CONSEJO):
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
