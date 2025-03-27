from __future__ import annotations

from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.postgres_db import get_db
from app.core.config import settings
from app.infraestructure.policies.application.application_flow import ApplicationFlow
from app.infraestructure.services.aws.s3 import s3
from app.schemas.application.user_application import UserApplicationPublic
from app.services.application.application_status import application_status_svc
from app.services.application.type.purchase import purchase_svc
from app.services.application.user_application import user_application_svc


class ApplicationType(str, Enum):
    PURCHASE = 'purchase'


SERVICES = {
    'purchase': purchase_svc,
}

APPLICATIONS_IDS = {
    'purchase': settings.PURCHASE_ID,
}


router = APIRouter()


@router.get('/{id}', response_model=UserApplicationPublic, status_code=200)
async def get_user_application(
    *,
    id: UUID,
    db_postgres: Session = Depends(get_db),
) -> UserApplicationPublic:
    user_application = user_application_svc.get(id=id, db=db_postgres)
    documents = s3.list_documents(
        bucket_name=settings.aws_bucket_name,
        user_id=user_application.user_id,
        user_application_id=user_application.id,
    )
    return UserApplicationPublic(**vars(user_application), documents=documents)


@router.post('/{user_application_id}/next', response_model=None, status_code=200)
async def advance_application_status(
    user_application_id: UUID,
    db_postgres: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_active_user),
    is_approved: bool = True,
    observation: Annotated[str, Form()] = '',
) -> JSONResponse:
    user_application = user_application_svc.get(id=user_application_id, db=db_postgres)
    application_flow = ApplicationFlow(user_application)

    response = await application_flow.next(
        is_approved=is_approved,
        observation=observation,
        db_postgres=db_postgres,
        current_user=current_user,
    )

    return response


@router.post('/upload/{id}', response_model=None, status_code=200)
async def upload_files(
    *,
    id: UUID,
    files: list[UploadFile],
    db_postgres: Session = Depends(get_db),
) -> JSONResponse:
    res = user_application_svc.upload_files(
        user_application_id=id, files=files, db=db_postgres,
    )
    return res


@router.get('/get_document/')
async def get_document(
    *,
    user_id: UUID,
    user_application_id: UUID,
    document_name: str,
):
    key: str = f'{user_id}/{user_application_id}/{document_name}'
    try:
        res = s3.get_data_from_s3_bucket(
            bucket_name=settings.aws_bucket_name, file_name=key,
        )
    except Exception:
        return JSONResponse(
            status_code=400,
            content={'error al intentar obtener el archivo:'},
        )
    return StreamingResponse(content=res['Body'], media_type=res['ContentType'])


@router.get(
    '/academic_unit/{academic_unit_id}',
    response_model=list[UserApplicationPublic],
    status_code=200,
)
async def get_user_application_to_academic_unit(
    *,
    academic_unit_id: UUID,
    db_postgres: Session = Depends(get_db),
) -> list[UserApplicationPublic]:
    user_applications = user_application_svc.get_by_academic_unit(
        academic_unit_id=academic_unit_id, db=db_postgres,
    )
    return [UserApplicationPublic.model_validate(app) for app in user_applications]


@router.get(
    '/user/{user_id}',
    response_model=list[UserApplicationPublic],
    status_code=200,
)
async def get_user_application_to_user(
    *,
    user_id: UUID,
    db_postgres: Session = Depends(get_db),
) -> list[UserApplicationPublic]:
    user_applications = user_application_svc.get_to_user(
        user_id=user_id, db=db_postgres,
    )
    return [UserApplicationPublic.model_validate(app) for app in user_applications]


@router.get('/next_step/{application_id}', status_code=200)
async def get_next_status(
    *,
    current_step: int,
    application_id: UUID,
    db_postgres: Session = Depends(get_db),
) -> str:
    next_status = application_status_svc.get_next_step(
        current_step=current_step,
        application_id=application_id,
        db=db_postgres,
    )
    return next_status
