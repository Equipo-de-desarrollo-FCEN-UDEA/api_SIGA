from __future__ import annotations

import logging
from datetime import datetime
from datetime import timedelta
from http import HTTPStatus
from typing import Annotated
from typing import Any
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import Security
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.api.middleware.scopes import has_role
from app.core.constants import COMMISION_ID
from app.core.constants import PROFESSOR_ROL_ID
from app.schemas.application.type.commission import Commission
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.type.commission import CommissionUpdate
from app.schemas.application.user_application import UserApplicationPublic
from app.schemas.users.user import User
from app.services.application.type.commission import commission_svc
from app.services.application.user_application import user_application_svc
from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc

log = logging.getLogger(__name__)

router = APIRouter()


@router.get('/{id}', response_model=Commission, status_code=200)
async def get_commission(
    *,
    id: UUID,
    db_mongo=Depends(get_mongo_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Commission:
    commission = await commission_svc.get(id=id, db=db_mongo)

    return Commission(**vars(commission))


@router.post('/create', response_model=UserApplicationPublic, status_code=201)
async def create_commission(
    *,
    country: Annotated[str, Form()],
    state: Annotated[str, Form()],
    city: Annotated[str, Form()],
    date_start: Annotated[datetime, Form()],
    date_end: Annotated[datetime, Form()],
    reason: Annotated[str, Form()],
    justification: Annotated[str, Form()],
    documents: Annotated[list[UploadFile], File()],
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    permissions: Annotated[
        bool, Security(
        has_role, scopes=['profesor'],
        ),
    ] = False,
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> UserApplicationPublic:
    obj_in = CommissionCreate(
        country=country,
        state=state,
        city=city,
        date_start=date_start,
        date_end=date_end,
        reason=reason,
        justification=justification,
        documents=[f'documento-{i+1}' for i in range(len(documents))],
    )

    if (date_end - date_start) >= timedelta(days=30):
        committee = user_rol_academic_unit_svc.get_student_committee(
            user_id=current_user.id, db=db_postgres,
        )
        academic_unit_id = committee

    else:
        get_units = user_rol_academic_unit_svc.get_academic_units_by_user_id_and_rol_id

        academic_unit_id = get_units(
            user_id=current_user.id,
            rol_id=UUID(PROFESSOR_ROL_ID),
            db=db_postgres,
        )

        academic_unit_id = academic_unit_id[0].id

    commission_create = await user_application_svc.create_user_application(
        obj_in=obj_in,
        current_user_id=current_user.id,
        application_id=UUID(COMMISION_ID),
        academic_unit_id=academic_unit_id,
        db_postgres=db_postgres,
        mongo_service=commission_svc,
        db_mongo=db_mongo,
    )

    return commission_create


@router.delete(
    '/{id}',
    response_model=str,
    status_code=HTTPStatus.OK.value,
    summary='Delete a commission by ID',
    description=(
        'Delete a specific commission by its unique ID. '
        'Authentication is required, and only users with the appropriate scope '
        'for professors or administrative personnel can access this endpoint.'
    ),
    responses={
        200: {'description': 'Commission successfully deleted.'},
        401: {'description': 'User not authenticated.'},
        404: {'description': 'Commission not found.'},
        500: {'description': 'Internal server error.'},
    },
)
async def delete_commission(
    *,
    id: UUID,
    db_mongo=Depends(get_mongo_db),
    permissions: Annotated[
        bool, Security(
        has_role, scopes=['profesor'],
        ),
    ] = False,
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> str:
    await commission_svc.delete(id=id, db=db_mongo)

    return JSONResponse(
        content='Comision eliminada correctamente',
        status_code=HTTPStatus.OK.value,
    )


@router.put(
    '/{id}',
    response_model=CommissionUpdate,
    status_code=HTTPStatus.OK.value,
    summary='Update a commission by ID',
    description=(
        'Update a specific commission by its unique ID. '
        'Authentication is required, and only users with the appropriate scope '
        'for professors or administrative personnel can access this endpoint.'
    ),
    responses={
        200: {
            'description': 'Commission successfully updated.',
            'content': {
                'application/json': {
                    'example': {
                        'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                        'country': 'Colombia',
                        'state': 'Antioquia',
                        'city': 'Medellin',
                        'date_start': '2025-01-16T15:57:37.890Z',
                        'date_end': '2025-01-16T15:57:37.890Z',
                        'reason': 'string',
                        'justification': 'string',
                        'status': [
                            {
                                'name': 'CREADA',
                                'updated_by': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                                'date': '2025-01-16T15:57:37.890Z',
                            },
                        ],
                        'documents': [
                            'string',
                        ],
                    },
                },
            },
        },
        400: {'description': 'Invalid data provided.'},
        401: {'description': 'User not authenticated.'},
        404: {'description': 'Commission not found.'},
        500: {'description': 'Internal server error.'},
    },
)
async def update_commission(
    *,
    id: UUID,
    obj_in: CommissionUpdate,
    db_mongo: Any = Depends(get_mongo_db),
    permissions: Annotated[
        bool, Security(
        has_role, scopes=['profesor'],
        ),
    ] = False,
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> CommissionUpdate:
    return await commission_svc.update(
        id=id,
        db_mongo=db_mongo,
        obj_in=obj_in,
    )


# @router.patch(
#     '/update-status/{id}',
#     response_model=str,
#     status_code=HTTPStatus.OK.value,
#     summary='Update the status of a commission',
#     description=(
#         'Update the status of a specific commission by its unique ID. '
#         'Authentication is required, and only users with the appropriate scope '
#         'for professors or administrative personnel can access this endpoint.'
#     ),
#     responses={
#         200: {'description': 'Commission status successfully updated.'},
#         401: {'description': 'User not authenticated.'},
#         404: {'description': 'Commission not found.'},
#         500: {'description': 'Internal server error.'},
#     },
# )
# async def update_status(
#     *,
#     id: UUID,
#     start_date: datetime | None,
#     end_date: datetime | None,
#     response: str,
#     db_mongo=Depends(get_mongo_db),
#     db_postgres: Session = Depends(get_db),
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ) -> str:
#     await flux(
#         start_date=start_date,
#         end_date=end_date,
#         user_application_id=id,
#         db_mongo=db_mongo,
#         db_postgres=db_postgres,
#         current_user=current_user,
#         response=response,
#     )
#     return JSONResponse(content='Status updated', status_code=HTTPStatus.OK.value)
