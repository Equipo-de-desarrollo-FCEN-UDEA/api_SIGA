from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import Security
from fastapi.responses import JSONResponse

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.api.middleware.scopes import has_role
from app.api.middleware.scopes import has_role_in_academic_unit
from app.infraestructure.policies.application.user_application_academic_unit import (
    response,
)
from app.protocols.db.models.application.user_application_academic_unit import (
    Result,
)
from app.schemas.application.user_application_academic_unit import (
    UserApplicationAcademicUnit,
)
from app.schemas.users.user import User
from app.services.application.user_application_academic_unit import (
    user_application_academic_unit_svc as us_app_svc,
)

router = APIRouter()


@router.get(
    '/get/{academic_unit_id}',
    response_model=list[UserApplicationAcademicUnit],
    status_code=200,
)
def get_user_application_academic_unit_by_academic_unit(
        academic_unit_id: UUID,
        *,
        db=Depends(get_db),
        user: User = Depends(has_role_in_academic_unit(role='representante')),

) -> list[UserApplicationAcademicUnit]:
    user_applications_academic_unit = us_app_svc.get_by_academic_unit(
        academic_unit_id=academic_unit_id, db=db,
    )

    user_applications = [
        UserApplicationAcademicUnit.model_validate(
            user_application_academic_unit.__dict__,
        )
        for user_application_academic_unit in user_applications_academic_unit
    ]
    return user_applications


@router.get(
    '/get/active/{user_application_id}/',
    response_model=UserApplicationAcademicUnit,
    status_code=200,
)
def get_active_user_application_academic_unit(
        user_application_id: UUID,
        *,
        db=Depends(get_db),
        user: User = Security(has_role, scopes=['representante']),
) -> UserApplicationAcademicUnit:
    user_application_academic_unit = us_app_svc.get_active(
        user_application_id=user_application_id, db=db,
    )
    return UserApplicationAcademicUnit.model_validate(
        user_application_academic_unit.__dict__,
    )


@router.patch(
    '/response/{user_application_id}/{academic_unit_id}',
    status_code=200,
)
async def approve_user_application_academic_unit(
        user_application_id: UUID,
        academic_unit_id: UUID,
        result: Result,
        *,
        db_postgres=Depends(get_db),
        db_mongo=Depends(get_mongo_db),
        permission: bool = Depends(
            has_role_in_academic_unit(role='representante'),
        ),
        user: User = Depends(get_current_active_user),
) -> Response:
    user_application_academic_unit = us_app_svc.response(
        user_application_id=user_application_id,
        academic_unit_id=academic_unit_id,
        db=db_postgres,
    )
    await response(
        user_application_academic_unit=user_application_academic_unit,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=user,
        result=result,
    )
    return JSONResponse(
        content={
            'message': 'User Application Academic Unit updated successfully',
        },
    )
