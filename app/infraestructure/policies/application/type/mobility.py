from __future__ import annotations

import os
from datetime import datetime
from tempfile import NamedTemporaryFile

from docx import Document
from fastapi import HTTPException

from app.infraestructure.policies.application.user_application import (
    create_voting,
)
from app.infraestructure.policies.application.user_application import (
    current_status,
)
from app.infraestructure.policies.application.user_application import (
    send_to_academic_unit,
)
from app.protocols.db.models.application.application import (
    ApplicationStatusType,
)
from app.schemas.application.user_application import UserApplicationStatus
from app.schemas.users.user import User
from app.services.application.type.mobility import mobility_svc
from app.services.users.user_rol_academic_unit import (
    user_rol_academic_unit_svc,
)

from app.core.config import settings


def next_status(current_status: str, response: str | None = None) -> str:
    if current_status == ApplicationStatusType.CREATE.value:
        return ApplicationStatusType.IN_COMMITEE.value
    elif current_status == ApplicationStatusType.IN_COMMITEE.value:
        if (response == 'APROBADA'):
            return ApplicationStatusType.IN_INTERNATIONAL.value
        elif (response == 'RECHAZADA'):
            return ApplicationStatusType.RETURNED.value
        else:
            return ApplicationStatusType.REJECTED.value
    elif current_status == ApplicationStatusType.IN_INTERNATIONAL.value:
        if (response == 'APROBADA'):
            return ApplicationStatusType.IN_DEAN.value
        elif (response == 'RECHAZADA'):
            return ApplicationStatusType.REJECTED.value
    elif current_status == ApplicationStatusType.IN_DEAN.value:
        if (response == 'APROBADA'):
            return ApplicationStatusType.APPROVED.value
        elif (response == 'RECHAZADA'):
            return ApplicationStatusType.REJECTED.value
    else:
        return None


async def flux(
    *,
    user_application_id,
    db_mongo,
    db_postgres,
    current_user: User,
    response: str | None = None,
) -> str:
    _current_status = await current_status(
        user_application_id,
        db_mongo, mobility_svc,
    )
    if _current_status == ApplicationStatusType.APPROVED.value:
        raise HTTPException(
            status_code=400, detail='Solicitud ya aprobada',
        )
    elif _current_status == ApplicationStatusType.REJECTED.value:
        raise  HTTPException(
            status_code=400, detail='Solicitud ya rechazada',
        )
    _next_status = next_status(_current_status, response)

    if _next_status == ApplicationStatusType.IN_COMMITEE.value:
        committee = user_rol_academic_unit_svc.get_student_committee(
            user_id=current_user.id, db=db_postgres,
        )
        send_to_academic_unit(
            academic_unit_id=committee,
            user_application_id=user_application_id, db=db_postgres,
        )
        await create_voting(
            academic_unit_id=committee,
            user_application_id=user_application_id,
            db_postgres=db_postgres,
            db_mongo=db_mongo,
        )
        status = UserApplicationStatus(
            name=_next_status,
            updated_by=current_user.id, date=datetime.now(),
        )

    elif _current_status == ApplicationStatusType.IN_COMMITEE.value:
        if response == 'APROBADA':
            send_to_academic_unit(
                academic_unit_id=settings.INTERNAL_FCEN,
                user_application_id=user_application_id, db=db_postgres,
            )
        status = UserApplicationStatus(
            name=_next_status,
            updated_by=current_user.id, date=datetime.now(),
        )

    elif _current_status == ApplicationStatusType.IN_INTERNATIONAL.value:
        if response == 'APROBADA':
            send_to_academic_unit(
                academic_unit_id=settings.FCEN,
                user_application_id=user_application_id, db=db_postgres,
            )
        status = UserApplicationStatus(
            name=_next_status,
            updated_by=current_user.id, date=datetime.now(),
        )
    elif _current_status == ApplicationStatusType.IN_DEAN.value:
        status = UserApplicationStatus(
            name=_next_status,
            updated_by=current_user.id, date=datetime.now(),
        )

    await mobility_svc.add_status(
        db_mongo=db_mongo,
        new_status=status,
        user_application_id=user_application_id,
    )


def generate_mobility_format(mobility_dict: dict, path: str):

    mobility_data = {
        'date': mobility_dict['status'][0]['date'].strftime('%Y-%m-%d'),

        'name': mobility_dict['name'] + ' ' + mobility_dict['last_name'],
        'phone': mobility_dict['phone'],
        'email': mobility_dict['email'],
        'identification_type': mobility_dict['identification_type']
        .replace('_', ' '),
        'identification_number': mobility_dict['identification_number'],
        'nationality': 'HAY QUE PEDIR LA NACIONALIDAD',
        'rol': mobility_dict['student_rol'],
        'school': mobility_dict['school'],
        'current_academic_program': mobility_dict['current_program'],
        'semester': 'HAY QUE PEDIR EL SEMESTRE',

        'name_coordinator': 'HAY QUE INVENTARLO',
        'phone_coordinator': 'HAY QUE INVENTARLO',
        'email_coordinator': 'HAY QUE INVENTARLO',

        'incoming_leaving': mobility_dict['type'].value.split()[0],
        'national_international': mobility_dict['type'].value.split()[1],
        'process': mobility_dict['process'].value,
        'destination_country': mobility_dict['destination_country'],
        'destination_institution': mobility_dict['destination_institution'],
        'academic_program': mobility_dict['academic_program'],

        'name_contact_person': mobility_dict['name_contact_person'],
        'cellphone_contact_person': mobility_dict['cellphone_contact_person'],
        'email_contact_person': mobility_dict['email_contact_person'],

        'date_start': mobility_dict['date_start'].strftime('%Y-%m-%d'),
        'date_end': mobility_dict['date_end'].strftime('%Y-%m-%d'),

        'code1': mobility_dict['code1'],
        'subject1': mobility_dict['subject1'],
        'recognized_code1': mobility_dict['recognized_code1'],
        'recognized_subject1': mobility_dict['recognized_subject1'],
        'code2': mobility_dict['code2'],
        'subject2': mobility_dict['subject2'],
        'recognized_code2': mobility_dict['recognized_code2'],
        'recognized_subject2': mobility_dict['recognized_subject2'],
        'code3': mobility_dict['code3'],
        'subject3': mobility_dict['subject3'],
        'recognized_code3': mobility_dict['recognized_code3'],
        'recognized_subject3': mobility_dict['recognized_subject3'],
        'code4': mobility_dict['code4'],
        'subject4': mobility_dict['subject4'],
        'recognized_code4': mobility_dict['recognized_code4'],
        'recognized_subject4': mobility_dict['recognized_subject4'],

        'signature': '',
        'signature_responsible': '',

        'date_report': mobility_dict['date_report'].strftime('%Y-%m-%d'),
    }

    try:
        document = Document(path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Error al cargar la plantilla: {str(e)}',
        )

    # Reemplazar placeholders en el documento
    for paragraph in document.paragraphs:
        for key, value in mobility_data.items():
            if f'{{{{{key}}}}}' in paragraph.text:
                paragraph.text = paragraph.text.replace(
                    f'{{{{{key}}}}}', value,
                )

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in mobility_data.items():
                    if f'{{{{{key}}}}}' in cell.text:
                        cell.text = cell.text.replace(f'{{{{{key}}}}}', value)

    # Crear archivo temporal para guardar el documento generado
    tmp_file = NamedTemporaryFile(delete=False, suffix='.docx')
    document.save(tmp_file.name)
    tmp_file.close()
    return tmp_file.name


def delete_file(file_path: str):
    """Función para eliminar el archivo después de la descarga."""
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f'Archivo no encontrado: {file_path}')
