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
from app.api.middleware.scopes import has_role
from app.infraestructure.formats import formats_dir
from app.infraestructure.policies.application.type.mobility import delete_file
from app.infraestructure.policies.application.type.mobility import flux
from app.infraestructure.policies.application.type.mobility import (
    generate_mobility_format,
)
from app.schemas.application.type.mobility import Mobility
from app.schemas.application.type.mobility import MobilityCreate
from app.schemas.users.user import User
from app.services.application.type.mobility import mobility_svc
from app.services.application.user_application import user_application_svc
from app.services.organization.academic_unit import academic_unit_svc


router = APIRouter()


@router.get('/{id}', response_model=Mobility, status_code=200)
async def get_mobility(
    *,
    id: UUID,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Mobility:
    mobility = await mobility_svc.get(id=id, db=db_mongo)

    return Mobility(**vars(mobility))


@router.post('/create', response_model=MobilityCreate, status_code=201)
async def create_mobility(
    *,
    obj_in: MobilityCreate,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    permissions: Annotated[bool, Security(has_role, scopes=['estudiante'])] = False,
    current_user: Annotated[
        User, Security(
            get_current_active_user,
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


@router.post('/generate-mobility-form/{id}')
async def download_mobility_form(
    id: UUID,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
):
    # Obtener los datos de la movilidad
    mobility = await mobility_svc.get(id=id, db=db_mongo)

    # Obtener el rol y el programa actual del usuario
    user_application = user_application_svc.get(id=mobility.id, db=db_postgres)

    rol = None
    current_program = None
    school_id = None

    for role in user_application.user.user_roles_academic_units:
        if role.rol.name in ['ESTUDIANTE PREGRADO', 'ESTUDIANTE POSTGRADO']:
            rol = vars(role.rol)
            current_program = vars(role.academic_unit)
            school_id = current_program['academic_unit_id']
            break

    if current_program:
        academic_unit = academic_unit_svc.get(id=school_id, db=db_postgres)
        school = academic_unit.name
    else:
        school = None
        academic_unit = None

    # Convertir los datos de la movilidad a un diccionario
    mobility_dict = {
        **vars(mobility),
        **vars(user_application.user),
        'student_rol': rol,
        'current_program': current_program,
        'school': school,
    }
    print(mobility_dict)

    for i in range(1, 5):

        subject = mobility_dict['subjects'][
            i -
            1
        ] if i <= len(mobility_dict['subjects']) else {}

        # Asignar las claves correspondientes con un valor vacío si no existe
        mobility_dict[f'code{i}'] = subject.get('extern_code', '')
        mobility_dict[f'subject{i}'] = subject.get('extern_name', '')
        mobility_dict[f'recognized_code{i}'] = subject.get('intern_code', '')
        mobility_dict[f'recognized_subject{i}'] = subject.get(
            'intern_name', '',
        )

    try:
        # Generar archivo temporal
        file_path = generate_mobility_format(
            mobility_dict, formats_dir +
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
        media_type=(
            'application/vnd.openxmlformats-officedocument'
            '-wordprocessingml.document'
        ),
    )

    return response
