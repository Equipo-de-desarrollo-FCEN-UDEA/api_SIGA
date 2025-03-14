from __future__ import annotations

from enum import Enum
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.middleware.postgres_db import get_db
from app.core.config import settings
from app.infraestructure.services.aws.s3 import s3
from app.schemas.application.user_application import UserApplicationPublic
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
    return UserApplicationPublic(**vars(user_application))


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
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={'error': f'Error: {str(e)}'},
        )
    return StreamingResponse(content=res['Body'], media_type=res['ContentType'])
