from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.infraestructure.formats import formats_dir
from app.infraestructure.policies.application.type.mobility import delete_file
from app.infraestructure.policies.application.type.mobility import flux
from app.infraestructure.policies.application.type.mobility import generate_mobility_format
from app.infraestructure.policies.application.type.mobility import mobility_data
from app.schemas.application.type.mobility import Mobility
from app.schemas.application.type.mobility import MobilityCreate
from app.schemas.users.user import User
from app.services.application.type.mobility import mobility_svc

router = APIRouter()


@router.get('/{id}', response_model=Mobility, status_code=200)
async def get_mobility(
    *,
    id: UUID,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Mobility:
    return await mobility_svc.get(id=id, db=db_mongo)


@router.post('/create', response_model=MobilityCreate, status_code=201)
async def create_mobility(
    *,
    obj_in: MobilityCreate,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[
        User, Security(
            get_current_active_user, scopes=[
                'estudiante:posgrado', 'estudiante:pregrado',
            ],
        ),
    ] = None,
) -> MobilityCreate:

    mobility_create = await mobility_svc.create(
        db_mongo=db_mongo,
        obj_in=obj_in,
        db_postgres=db_postgres,
        current_user=current_user,
        application_id='1c779ce5-ce77-49ea-87e2-69a2388e53f2',
    )

    return mobility_create


@router.patch('/update/{id}', response_model=str, status_code=200)
async def update_status(
    *,
    id: UUID,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Mobility:

    await flux(
        user_application_id=id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
    )
    return JSONResponse(content='Status updated', status_code=200)


@router.post('/generate-mobility-form/')
async def download_mobility_form(background_tasks: BackgroundTasks):
    # Rellenar datos de la solicitud.
    try:
        # Generar archivo temporal
        file_path = generate_mobility_format(
            mobility_data, formats_dir +
            '/mobility/plantilla_mobility.docx',
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Error generando el archivo: {str(e)}',
        )

    background_tasks.add_task(delete_file, file_path)

    # Descargar el archivo y eliminarlo al finalizar
    response = FileResponse(
        file_path,
        filename='solicitud_mobility.docx',
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )

    return response
