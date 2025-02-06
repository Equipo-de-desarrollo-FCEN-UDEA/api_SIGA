from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, Security

from app.api.middleware.bearer import get_current_active_user
from app.schemas.application.user_application_academic_unit import UserApplicationAcademicUnitInDB
from app.schemas.application.user_application import UserApplicationInfo

from app.infraestructure.db.models.application.user_application_academic_unit import UserApplicationAcademicUnit
from app.services.application.user_application_academic_unit import user_application_academic_unit_svc as us_app_svc


from app.api.middleware.postgres_db import get_db

router = APIRouter()

@router.get("/get/{academic_unit_id}", response_model=list[UserApplicationInfo], status_code=200)
def get_user_application_academic_unit_by_academic_unit(
        *, academic_unit_id: UUID, 
        db = Depends(get_db), 
        user = Security(get_current_active_user, scopes=["representante"])
    ) -> list[UserApplicationInfo]:
    user_applications_academic_unit = us_app_svc.get_by_academic_unit(academic_unit_id=academic_unit_id, db=db)

    user_applications = [
        UserApplicationInfo.model_validate(
            user_application_academic_unit.user_application
        )
        for user_application_academic_unit in user_applications_academic_unit
    ]
    return user_applications
    