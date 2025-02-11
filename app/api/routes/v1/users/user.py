from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.scopes import has_scope
from app.api.middleware.scopes import has_role
from app.api.middleware.bearer import get_current_user
from app.api.middleware.postgres_db import get_db
from app.schemas.users.user import User, UserSession
from app.schemas.users.user import UserCreate
from app.schemas.users.user import UserInDB
from app.schemas.users.user import UserUpdate
from app.schemas.users.user import UserPublic
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnit
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnitCreate
from app.services.users.user import user_svc
from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc

router = APIRouter()


@router.post('', response_model=UserInDB, status_code=201)
def create_user(
    *, new_user: UserCreate, rol_id: UUID,
        academic_unit_id: UUID, db_postgres=Depends(get_db), ) -> UserInDB:
    user = user_svc.create(obj_in=new_user, db=db_postgres)
    user_rol_academic_unit_svc.create(
        obj_in=UserRolAcademicUnitCreate(
            rol_id=rol_id,
            user_id=user.id,
            academic_unit_id=academic_unit_id,
        ),
        db=db_postgres,
    )
    return user


@router.get('', response_model=list[UserInDB], status_code=200)
def get_all_user(
    *, skip: int = 0,
    limit: int = 10,
    db_postgres=Depends(get_db),
    current_user: Annotated[
        User, Security(
        has_role, scopes=['admin'],
        ),
    ] = None,
) -> list[UserInDB]:
    return user_svc.get_multi(skip=skip, limit=limit, db=db_postgres)


@router.get('/{id}', response_model=User, status_code=200)
def get_user(*, id: UUID, db_postgres=Depends(get_db)) -> User:
    user = user_svc.get(id=id, db=db_postgres)
    if not user:
        raise HTTPException(404, 'User not found')
    user = UserInDB.model_validate(user)
    roles = user_rol_academic_unit_svc.get_by_user_id(
        user_id=id, db=db_postgres,
    )

    user_roles_academic_units = [
        UserRolAcademicUnit.model_validate(role) for role in roles
    ]

    response = User(
        **user.model_dump(),
        user_roles_academic_units=user_roles_academic_units,
    )
    return response


@router.patch('/{id}', response_model=None)
def update_user(*, obj_in: UserUpdate, id: int) -> None:
    user = user_svc.get(id=id)
    if not user:
        raise HTTPException(404, 'User not found')
    user_svc.update(id=id, obj_in=obj_in)
    return None


@router.delete('/{id}', response_model=None, status_code=204)
def delete_user(*, id: int) -> None:
    user = user_svc.delete(id=id)
    if user == 0:
        raise HTTPException(404, 'User not found')
    return None


@router.get('/view/me', response_model=UserInDB, status_code=200)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> UserInDB:
    return current_user

@router.get('/session/me', response_model=UserSession, status_code=200)
async def get_session(current_user: Annotated[User, Depends(get_current_user)]) -> UserSession:
    return current_user
