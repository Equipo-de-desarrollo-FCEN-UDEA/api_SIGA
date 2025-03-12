from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.core.config import settings
from app.infraestructure.formats import formats_dir
from app.infraestructure.policies.application.type.purchase import delete_file
from app.infraestructure.policies.application.type.purchase import generate_format
from app.infraestructure.policies.application.type.purchase import PurchaseFlow
from app.protocols.db.models.application.type.purchase import ApprovedAcademicsUnits
from app.schemas.application.type.purchase import PurchaseComplete
from app.schemas.application.type.purchase import PurchaseCreate
from app.schemas.application.user_application import UserApplicationPublic
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
        User | None, Security(
            get_current_active_user,
        ),
    ] = None,
) -> PurchaseCreate:
    purchase = await purchase_svc.get(id=id, db=db_mongo)
    return purchase


@router.post('/create', response_model=UserApplicationPublic, status_code=201)
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
) -> UserApplicationPublic:
    purchase_create = await user_application_svc.create_user_application(
        obj_in=obj_in,
        current_user_id=current_user.id,
        application_id=settings.PURCHASE_ID,
        academic_unit_id=UUID(academic_unit_id.value),
        db_postgres=db_postgres,
        mongo_service=purchase_svc,
        db_mongo=db_mongo,
    )

    return purchase_create


class ApplicationRequest(BaseModel):
    user_to_assign_id: UUID | None = None
    observation: str | None = None
    purchase_complete: PurchaseComplete | None = None


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
    user_application = user_application_svc.get(id=user_application_id, db=db_postgres)
    application_flow = PurchaseFlow(user_application)

    # Ejecutar la transición con los argumentos dinámicos
    response = await application_flow.next(
        user_application_id=user_application_id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        is_approved=is_approved,
        **request.dict(exclude_unset=True),  # Pasar solo los valores proporcionados
    )

    return response


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

    # Obtener el nombre de la unidad academica
    if not user_application.user_application_academic_units:
        raise HTTPException(
            status_code=500,
            detail="La solicitud 'aún no ha sido aprobada por la unidad académica",
        )

    academic_unit_name = user_application.user_application_academic_units[
        0
    ].academic_unit.name

    # Diccionario con los datos necesarios del formato
    purchase_dict = {
        **vars(purchase),
        'academic_unit': academic_unit_name,
    }

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
        headers={'Content-Disposition': 'attachment; filename=solicitud_compra.docx'},
    )

    return res
