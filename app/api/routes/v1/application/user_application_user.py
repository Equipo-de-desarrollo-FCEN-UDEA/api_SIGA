from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from app.api.middleware.bearer import get_current_user_db
from app.api.middleware.postgres_db import get_db
from app.schemas.application.user_application_user import UserApplicationUserPublic
from app.schemas.users.user import User
from app.services.application.user_application_user import user_application_user_svc


router = APIRouter()


@router.get('/me', response_model=list[UserApplicationUserPublic])
def get_user_application_user_for_current_user(
    postgres_db=Depends(get_db),
    current_user: User = Depends(get_current_user_db),
) -> list[UserApplicationUserPublic]:
    user_applications_user = user_application_user_svc.get_by_user(
        user_id=current_user.id, db=postgres_db,
    )
    return user_applications_user
