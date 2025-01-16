from __future__ import annotations

import logging
from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.type.commission import CommissionResponse
from app.schemas.users.user import User
from app.services.application.type.commission import commission_svc

log = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    '/',
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
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
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
    '/{commission_id}',
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
    commission_id: UUID,
    db_mongo=Depends(get_mongo_db),
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> CommissionResponse:
    return await commission_svc.get(
        id=commission_id,
        db=db_mongo,
    )


@router.delete(
    '/{commission_id}',
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
    commission_id: UUID,
    db_mongo=Depends(get_mongo_db),
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> str:
    await commission_svc.delete(
        id=commission_id,
        db=db_mongo,
    )
    return 'Commission successfully deleted.'
