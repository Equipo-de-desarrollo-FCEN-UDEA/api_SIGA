from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.middleware.postgres_db import get_db
from app.schemas.application.user_application import UserApplicationPublic
from app.services.application.user_application import user_application_svc


router = APIRouter()


@router.get('/{id}', response_model=UserApplicationPublic, status_code=200)
async def get_user_application(
    *,
    id: UUID,
    db_postgres: Session = Depends(get_db),
) -> UserApplicationPublic:
    user_application = user_application_svc.get(id=id, db=db_postgres)
    return UserApplicationPublic(**vars(user_application))
