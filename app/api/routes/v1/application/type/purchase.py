from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi import UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.core.config import settings
from app.infraestructure.formats import formats_dir
from app.infraestructure.policies.application.type.purchase import delete_file
from app.infraestructure.policies.application.type.purchase import flux
from app.infraestructure.policies.application.user_application import (
    send_to_academic_unit,
)
from app.infraestructure.policies.application.type.purchase import generate_format
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
from app.services.application.user_application import user_application_svc

router = APIRouter()


@router.get('/{id}', response_model=PurchaseCreate, status_code=200)
async def get_purchase(
    *,
    id: UUID,
    db_mongo=Depends(get_mongo_db),
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> PurchaseCreate:
    return await purchase_svc.get(id=id, db=db_mongo)


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


@router.post('/generate-purchase-form/{id}')
async def download_purchase_form(
    id: UUID,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
):
    # Obtener los datos de la movilidad
    purchase = await purchase_svc.get(id=id, db=db_mongo)
    user_application = user_application_svc.get(id=id, db=db_postgres)

    academic_unit_name = user_application.user_application_academic_units[
        0
    ].academic_unit.name

    purchase_dict = {
        **vars(purchase),
        'academic_unit': academic_unit_name,
        # 'student_rol': rol,
        # 'current_program': current_program,
        # 'school': school,
    }
    print(type(purchase_dict))

    try:
        # Generar archivo temporal
        file_path = generate_format(
            purchase_dict, formats_dir +
            '/purchase/purchase_format.docx',
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Error generando el archivo: {str(e)}',
        )

    background_tasks.add_task(delete_file, file_path)

    # Descargar el archivo y eliminarlo al finalizar
    res = FileResponse(
        file_path,
        filename='solicitud_compra.docx',
        media_type=(
            'application/vnd.openxmlformats-officedocument'
            '-wordprocessingml.document'
        ),
    )

    return res
