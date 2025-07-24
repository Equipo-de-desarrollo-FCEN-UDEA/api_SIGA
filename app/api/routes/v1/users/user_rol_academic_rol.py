from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.api.middleware.postgres_db import get_db
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitCreate
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitInDB
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitPublic
from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc

router = APIRouter()


@router.post('', response_model=UserRolAcademicUnitInDB, status_code=201)
def create_user_rol(
    *,
    new_user_rol: UserRolAcademicUnitCreate,
    db_postgres=Depends(get_db),
) -> UserRolAcademicUnitInDB:
    response = user_rol_academic_unit_svc.create(obj_in=new_user_rol, db=db_postgres)
    return UserRolAcademicUnitInDB.model_validate(response)


@router.get('', response_model=list[UserRolAcademicUnitInDB], status_code=200)
def get_all_rol(
    *,
    skip: int = 0,
    limit: int = 10,
    db_postgres=Depends(get_db),
) -> list[UserRolAcademicUnitInDB]:
    response = user_rol_academic_unit_svc.get_multi(
        skip=skip, limit=limit, db=db_postgres,
    )
    return [UserRolAcademicUnitInDB.model_validate(rol) for rol in response]


# @router.get("/{academic_unit_id}",
#     response_model=list[UserRolAcademicUnitPublic],
#     status_code=200,
# )
@router.get(
    '/{academic_unit_id}/',
    response_model=list[UserRolAcademicUnitPublic],
    status_code=200,
)
def get_by_academic_unit_id(
    *,
    academic_unit_id: UUID,
    rol_name: str | None = None,
    db_postgres=Depends(get_db),
) -> list[UserRolAcademicUnitPublic]:
    response = user_rol_academic_unit_svc.get_by_academic_unit_id(
        academic_unit_id=academic_unit_id,
        rol_name=rol_name,
        db=db_postgres,
    )
    return [UserRolAcademicUnitPublic.model_validate(rol) for rol in response]
