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
from app.core import constants
from app.infraestructure.formats import formats_dir
from app.infraestructure.policies.application.type.mobility import delete_file
from app.infraestructure.policies.application.type.mobility import flux
from app.infraestructure.policies.application.type.mobility import (
    generate_format,
)
from app.schemas.application.type.mobility import Mobility
from app.schemas.application.type.mobility import MobilityCreate
from app.schemas.application.user_application import UserApplicationPublic
from app.schemas.users.user import User
from app.services.application.type.mobility import mobility_svc
from app.services.application.user_application import user_application_svc
from app.services.organization.academic_unit import academic_unit_svc
from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc


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


@router.post('/create', response_model=UserApplicationPublic, status_code=201)
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
) -> UserApplicationPublic:

    committee = user_rol_academic_unit_svc.get_student_committee(
        user_id=current_user.id, db=db_postgres,
    )

    mobility_create = await user_application_svc.create_user_application(
        obj_in=obj_in,
        current_user_id=current_user.id,
        application_id=constants.MOBILITY_ID,
        academic_unit_id=committee,
        db_postgres=db_postgres,
        mongo_service=mobility_svc,
        db_mongo=db_mongo,
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

    for i in range(1, 5):

        subject = mobility_dict['subjects'][
            i - 1
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
        file_path = generate_format(
            mobility_dict, formats_dir +
            '/mobility/mobility_format.docx',
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Error generando el archivo: {str(e)}',
        )

    background_tasks.add_task(delete_file, file_path)

    # Descargar el archivo y eliminarlo al finalizar
    res = FileResponse(
        file_path,
        filename='solicitud_de_movilidad.docx',
        media_type=(
            'application/vnd.openxmlformats-officedocument'
            '-wordprocessingml.document'
        ),
    )

    return res
