from __future__ import annotations

import logging
from datetime import datetime
from datetime import timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import Security
from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.api.middleware.scopes import has_role
from app.core.constants import COMMISSION_ID
from app.core.constants import PROFESSOR_ROL_ID
from app.infraestructure.policies.application.type.commission import CommissionFlow
from app.schemas.application.type.commission import Commission
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.user_application import UserApplicationPublic
from app.schemas.users.user import User
from app.services.application.type.commission import commission_svc
from app.services.application.user_application import user_application_svc
from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc

log = logging.getLogger(__name__)

router = APIRouter()


@router.get('/{id}', response_model=Commission, status_code=200)
async def get_commission(
    *,
    id: UUID,
    db_mongo=Depends(get_mongo_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Commission:
    commission = await commission_svc.get(id=id, db=db_mongo)

    return Commission(**vars(commission))


@router.post('/create', response_model=UserApplicationPublic, status_code=201)
async def create_commission(
    *,
    country: Annotated[str, Form()],
    state: Annotated[str, Form()],
    city: Annotated[str, Form()],
    date_start: Annotated[datetime, Form()],
    date_end: Annotated[datetime, Form()],
    reason: Annotated[str, Form()],
    justification: Annotated[str, Form()],
    documents: Annotated[list[UploadFile], File()],
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    permissions: Annotated[
        bool, Security(
        has_role, scopes=['profesor'],
        ),
    ] = False,
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> UserApplicationPublic:

    obj_in = CommissionCreate(
        country=country,
        state=state,
        city=city,
        date_start=date_start,
        date_end=date_end,
        reason=reason,
        justification=justification,
        documents=[f'documento-{i+1}' for i in range(len(documents))],
    )

    # Si el rango de fechas es mayor a 30 días, se manda a votación

    if (date_end - date_start) >= timedelta(days=30):
        committee = user_rol_academic_unit_svc.get_student_committee(
            user_id=current_user.id, db=db_postgres,
        )
        academic_unit_id = committee

    # If the date range is less than 30 days, it is sent to the academic unit

    else:
        get_units = user_rol_academic_unit_svc.get_academic_units_by_user_id_and_rol_id

        academic_unit_id = get_units(
            user_id=current_user.id,
            rol_id=UUID(PROFESSOR_ROL_ID),
            db=db_postgres,
        )

        academic_unit_id = academic_unit_id[0].id

    commission_create = await user_application_svc.create_user_application(
        obj_in=obj_in,
        current_user_id=current_user.id,
        application_id=UUID(COMMISSION_ID),
        academic_unit_id=academic_unit_id,
        db_postgres=db_postgres,
        mongo_service=commission_svc,
        db_mongo=db_mongo,
    )

    user_application_svc.upload_files(
        user_application_id=commission_create.id,
        files=documents,
        db=db_postgres,
        prefix='documento',
    )

    return commission_create


class ApplicationRequest(BaseModel):
    academic_unit_id: UUID | None = None


@router.post('/{user_application_id}/next', response_model=None)
async def advance_application_status(
    user_application_id: str,
    request: ApplicationRequest,
    is_approved: bool = True,
    db_mongo=Depends(get_mongo_db),
    db_postgres=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Endpoint para avanzar el estado de una solicitud.
    """

    # Obtener la solicitud
    user_application = user_application_svc.get(id=user_application_id, db=db_postgres)

    # Instanciar el flujo de movilidad
    application_flow = CommissionFlow(user_application)

    # Ejecutar la transición con los argumentos dinámicos
    response = await application_flow.next(
        user_application_id=user_application_id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        is_approved=is_approved,
        **request.model_dump(exclude_unset=True),
    )

    return response
