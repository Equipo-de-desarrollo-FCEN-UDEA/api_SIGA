from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.users.user import User
from app.services.application.type.commission import commission_svc

log = logging.getLogger(__name__)

router = APIRouter()

CREATED = 201
OK = 200


@router.post(
    '/',
    response_model=CommissionCreate,
    status_code=CREATED,
    summary='Create a new commission',
    description=(
        'Endpoint to create a new commission. This requires authentication '
        'and the appropriate scope for professors or administrative personnel.'
    ),
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
    """
    Create a new commission.

    Args:
        obj_in (CommissionCreate): Data for the new commission.
        db_mongo: Dependency to interact with MongoDB.
        db_postgres (Session): Dependency to interact with PostgreSQL.
        current_user (User): The currently authenticated user.

    Returns:
        CommissionCreate: The created commission object.

    Raises:
        HTTPException: If the user is not authenticated, lacks permissions,
                        or an error occurs during creation.

    Possible responses:
        - **201**: Commission successfully created.
        - **400**: Invalid data provided.
        - **401**: User not authenticated.
        - **500**: Internal server error.
    """

    return await commission_svc.create(
        db_mongo=db_mongo,
        obj_in=obj_in,
        db_postgres=db_postgres,
        current_user=current_user,
        application_id='21444ff5-eecc-4365-aad9-ccce45b7d48f',
    )
