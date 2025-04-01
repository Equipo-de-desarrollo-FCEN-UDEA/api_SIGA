from __future__ import annotations

import logging
from datetime import datetime
from http import HTTPStatus
from typing import Annotated
from typing import Any
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.api.middleware.scopes import has_role
from app.infraestructure.policies.application.type.commission import flux
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.type.commission import CommissionResponse
from app.schemas.application.type.commission import CommissionUpdate
from app.schemas.users.user import User
from app.services.application.type.commission import commission_svc

log = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    '/create',
    response_model=CommissionCreate,
    status_code=HTTPStatus.CREATED.value,
    summary='Create a new commission',
    description=(
        'Create a new commission by providing the necessary details. '
        'Authentication is required, and only users with the appropriate scope '
        'for professors or administrative personnel can access this endpoint.'
    ),
    responses={
        201: {
            'description': 'Commission successfully created.',
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
        500: {'description': 'Internal server error.'},
    },
)
async def create_commission(
    *,
    obj_in: CommissionCreate,
    db_mongo: Any = Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    permissions: Annotated[bool, Security(has_role, scopes=['profesor'])] = False,
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> CommissionCreate:
    return await commission_svc.create(
        db_mongo=db_mongo,
        obj_in=obj_in,
        db_postgres=db_postgres,
        current_user=current_user,
        application_id='21444ff5-eecc-4365-aad9-ccce45b7d48f',
    )


@router.get(
    '/{id}',
    response_model=CommissionResponse,
    status_code=HTTPStatus.OK.value,
    summary='Get a commission by ID',
    description=(
        'Retrieve a specific commission by its unique ID. '
        'Authentication is required, and only users with the appropriate scope '
        'for professors or administrative personnel can access this endpoint.'
    ),
    responses={
        200: {
            'description': 'Commission successfully retrieved.',
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
        401: {'description': 'User not authenticated.'},
        404: {'description': 'Commission not found.'},
        500: {'description': 'Internal server error.'},
    },
)
async def get_commission(
    *,
    id: UUID,
    db_mongo: Any = Depends(get_mongo_db),
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> CommissionResponse:
    return await commission_svc.get(id=id, db=db_mongo)


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
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> str:
    await commission_svc.delete(id=id, db=db_mongo)

    return JSONResponse(content='Commission successfully deleted.', status_code=HTTPStatus.OK.value)


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
    db_postgres: Session = Depends(get_db),
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
        db_postgres=db_postgres,
        current_user=current_user,
    )


@router.patch(
    '/update-status/{id}',
    response_model=str,
    status_code=HTTPStatus.OK.value,
    summary='Update the status of a commission',
    description=(
        'Update the status of a specific commission by its unique ID. '
        'Authentication is required, and only users with the appropriate scope '
        'for professors or administrative personnel can access this endpoint.'
    ),
    responses={
        200: {'description': 'Commission status successfully updated.'},
        401: {'description': 'User not authenticated.'},
        404: {'description': 'Commission not found.'},
        500: {'description': 'Internal server error.'},
    },
)
async def update_status(
    *,
    id: UUID,
    start_date: datetime | None,
    end_date: datetime | None,
    response: str,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> str:
    await flux(
        start_date=start_date,
        end_date=end_date,
        user_application_id=id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        response=response,
    )
    return JSONResponse(content='Status updated', status_code=HTTPStatus.OK.value)
