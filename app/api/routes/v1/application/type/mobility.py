from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.infraestructure.policies.application.type.mobility import flux
from app.schemas.application.type.mobility import Mobility
from app.schemas.application.type.mobility import MobilityCreate
from app.schemas.users.user import User
from app.services.application.type.mobility import mobility_svc


router = APIRouter()


@router.post('/create', response_model=MobilityCreate, status_code=201)
async def create_mobility(
    *,
    obj_in: MobilityCreate,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[
        User, Security(
            get_current_active_user, scopes=[
                'estudiante:posgrado', 'estudiante:pregrado',
            ],
        ),
    ] = None,
) -> MobilityCreate:

    mobility_create = await mobility_svc.create(
        db_mongo=db_mongo,
        obj_in=obj_in,
        db_postgres=db_postgres,
        current_user=current_user,
        application_id='1c779ce5-ce77-49ea-87e2-69a2388e53f2',
    )

    return mobility_create


@router.patch('/update/{id}', response_model=str, status_code=200)
async def update_status(
    *,
    id: UUID,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Mobility:

    await flux(
        user_application_id=id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
    )
    return JSONResponse(content='Status updated', status_code=200)
