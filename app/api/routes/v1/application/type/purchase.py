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
from app.core.config import settings
from app.infraestructure.policies.application.type.purchase import flux
from app.protocols.db.models.application.type.purchase import ApprovedAcademicsUnits
from app.schemas.application.type.purchase import PurchaseComplete
from app.schemas.application.type.purchase import PurchaseCreate
from app.schemas.users.user import User
from app.services.application.type.purchase import purchase_svc


router = APIRouter()


@router.post('/create', response_model=PurchaseCreate, status_code=201)
async def create_purchase(
    *,
    obj_in: PurchaseCreate,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> PurchaseCreate:
    purchase_create = await purchase_svc.create(
        obj_in=obj_in,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        application_id=settings.PURCHASE_ID,
    )

    return purchase_create


@router.patch('/send/{id}', response_model=None, status_code=200)
async def send_to_academic_unit(
    *,
    id: UUID,
    academic_unit_id: ApprovedAcademicsUnits,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> JSONResponse:
    res = await flux(
        user_application_id=id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        is_approved=True,
        academic_unit_id=UUID(academic_unit_id.value),
    )

    return res


@router.patch('/send/user/{id}', response_model=None, status_code=200)
async def assing_auxiliary(
    *,
    id: UUID,
    user_id: UUID,
    is_approved: bool,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> JSONResponse:
    res = await flux(
        user_application_id=id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        is_approved=is_approved,
        user_to_assign=user_id,
    )

    return res


@router.patch('/complete/{id}', response_model=None, status_code=200)
async def update_purchase(
    *,
    id: UUID,
    obj_in: PurchaseComplete,
    is_approved: bool,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> JSONResponse:
    res = await flux(
        user_application_id=id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        is_approved=is_approved,
        obj_in=obj_in,
    )

    return res


@router.patch('/next/{id}', response_model=None, status_code=200)
async def next_status(
    *,
    id: UUID,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
    is_approved: bool,
) -> JSONResponse:
    res = await flux(
        user_application_id=id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        is_approved=is_approved,
    )

    return res
