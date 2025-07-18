from __future__ import annotations

import json
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import Security
from fastapi import UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.api.middleware.scopes import has_role
from app.core import constants
from app.infraestructure.formats import formats_dir
from app.infraestructure.policies.application.type.mobility import delete_file
from app.infraestructure.policies.application.type.mobility import (
    generate_format,
)
from app.infraestructure.policies.application.type.mobility import MobilityFlow
from app.protocols.db.models.application.type.mobility import MobilityPurpose
from app.protocols.db.models.application.type.mobility import MobilityType
from app.protocols.db.models.application.type.mobility import Process
from app.schemas.application.type.mobility import Mobility
from app.schemas.application.type.mobility import MobilityCreate
from app.schemas.application.type.mobility import Subject
from app.schemas.application.user_application import UserApplicationPublic
from app.schemas.application.user_application_academic_unit import (
    UserApplicationAcademicUnitCreate,
)
from app.schemas.users.user import User
from app.services.application.type.mobility import mobility_svc
from app.services.application.user_application import user_application_svc
from app.services.application.user_application_academic_unit import (
    user_application_academic_unit_svc,
)
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
    process: Annotated[Process, Form()],
    type: Annotated[MobilityType, Form()],
    purpose: Annotated[MobilityPurpose, Form()],
    destination_country: Annotated[str, Form()],
    destination_institution: Annotated[str, Form()],
    academic_program: Annotated[str, Form()],
    name_contact_person: Annotated[str, Form()],
    cellphone_contact_person: Annotated[str, Form()],
    email_contact_person: Annotated[str, Form()],
    date_start: Annotated[datetime, Form()],
    date_end: Annotated[datetime, Form()],
    subjects: Annotated[list[str], Form()] = [],
    admission_letter: Annotated[UploadFile, File()],
    enrollment_certificate: Annotated[UploadFile, File()],
    insurance: Annotated[UploadFile | None, File()] = None,
    passport: Annotated[UploadFile | None, File()] = None,
    db_mongo=Depends(get_mongo_db),
    db_postgres: Session = Depends(get_db),
    permissions: Annotated[bool, Security(has_role, scopes=['estudiante'])] = False,
    current_user: Annotated[
        User, Security(
            get_current_active_user,
        ),
    ] = None,
) -> UserApplicationPublic:
    documents = [admission_letter, enrollment_certificate, insurance, passport]
    documents = [doc for doc in documents if doc is not None]
    parsed_subjects = []
    if subjects:
        subjects_str = f'[{subjects[0]}]'
        try:
            parsed_subjects = [Subject(**item) for item in json.loads(subjects_str)]
        except Exception:
            raise HTTPException(status_code=422, detail="Formato inválido de 'subjects'")

    obj_in = MobilityCreate(
        process=process,
        type=type,
        purpose=purpose,
        destination_country=destination_country,
        destination_institution=destination_institution,
        academic_program=academic_program,
        name_contact_person=name_contact_person,
        cellphone_contact_person=cellphone_contact_person,
        email_contact_person=email_contact_person,
        date_start=date_start,
        date_end=date_end,
        total_time=(date_end - date_start).days,
        subjects=parsed_subjects,
    )

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

    # Cálculo de del instituto/departamento y facultad

    institute_id = academic_unit_svc.get(
        id=committee, db=db_postgres,
    ).academic_unit_id
    faculty_id = academic_unit_svc.get(
        id=institute_id, db=db_postgres,
    ).academic_unit_id

    user_application_academic_unit = UserApplicationAcademicUnitCreate(
        user_application_id=mobility_create.id,
        academic_unit_id=faculty_id,
    )
    user_application_academic_unit_svc.create(
        obj_in=user_application_academic_unit,
        db=db_postgres,
    )

    user_application_svc.upload_files(
        user_application_id=mobility_create.id,
        files=documents,
        db=db_postgres,
        prefix=None,
    )

    return mobility_create


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
    Endpoint para avanzar el estado de una solicitud de movilidad.
    """
    # Obtener la solicitud
    user_application = user_application_svc.get(id=user_application_id, db=db_postgres)

    # Instanciar el flujo de movilidad
    application_flow = MobilityFlow(user_application)

    # Ejecutar la transición
    response = await application_flow.next(
        user_application_id=user_application_id,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        is_approved=is_approved,
        **request.model_dump(exclude_unset=True),
    )

    return response


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
