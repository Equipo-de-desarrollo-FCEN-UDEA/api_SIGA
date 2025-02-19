from __future__ import annotations

from datetime import datetime
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
from app.infraestructure.db.models.application.type.purchase import Purchase
from app.infraestructure.policies.application.type.purchase import flux
from app.schemas.application.type.purchase import PurchaseCreate
from app.schemas.application.user_application import UserApplicationCreate
from app.schemas.application.user_application import UserApplicationStatus
from app.schemas.users.user import User
from app.services.application.type.purchase import purchase_svc
from app.services.application.user_application import user_application_svc


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
    academic_unit_id: UUID,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> JSONResponse:
    purchase = await purchase_svc.get(id=id, db=db_mongo)
    return JSONResponse(
        status_code=200,
        content={
            'message': 'Solicitud enviada a la unidad académica',
        },
    )
