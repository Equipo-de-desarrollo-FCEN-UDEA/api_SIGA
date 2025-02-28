from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.core.config import settings
from app.infraestructure.policies.application.type.purchase import flux
from app.infraestructure.policies.application.user_application import (
    send_to_academic_unit,
)
from app.protocols.db.models.application.type.purchase import ApprovedAcademicsUnits
from app.schemas.application.type.purchase import Material
from app.schemas.application.type.purchase import Provider
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
    academic_unit_id: ApprovedAcademicsUnits,
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

    send_to_academic_unit(
        user_application_id=purchase_create.id,
        academic_unit_id=UUID(academic_unit_id.value),
        db=db_postgres,
    )

    return purchase_create


@router.post('/upload/{id}', response_model=None, status_code=200)
async def upload_files(
    *,
    id: UUID,
    files: list[UploadFile],
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
        files=files,
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


@router.patch('/{id}', response_model=None, status_code=200)
async def select_provider(
    *,
    id: UUID,
    provider: Provider,
    materials: list[Material],
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
        provider=provider,
        materials=materials,
    )

    return res
