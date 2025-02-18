from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.core.config import settings
from app.infraestructure.db.models.application.type.purchase import Purchase
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
    user_application_create = UserApplicationCreate(
        user_id=current_user.id, application_id=settings.PURCHASE_ID,
    )
    user_application = user_application_svc.create(
        obj_in=user_application_create, db=db_postgres,
    )
    obj_in.id = user_application.id

    create_status = UserApplicationStatus(
        name='CREADA',
        updated_by=current_user.id,
        date=datetime.now(),
    )
    obj_in.status = [create_status]

    purchase_create = await purchase_svc.create(
        obj_in=Purchase(**dict(obj_in)),
        db=db_mongo,
    )

    return purchase_create
