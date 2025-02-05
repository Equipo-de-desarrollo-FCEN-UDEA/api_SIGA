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
# from fastapi import FastAPI
# from fastapi.responses import FileResponse
# from app.schemas.application.type.mobility import MobilityResponse


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
            return ApplicationStatusType.RETURNED.value
    elif current_status == ApplicationStatusType.IN_DEAN.value:
        if (response == 'APROBADA'):
            return ApplicationStatusType.APPROVED.value
        elif (response == 'RECHAZADA'):
            return ApplicationStatusType.RETURNED.value
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
    _next_status = next_status(_current_status, response)
    print(_next_status)
    committee = user_rol_academic_unit_svc.get_student_committee(
        user_id=current_user.id, db=db_postgres,
    )

    if _next_status == ApplicationStatusType.IN_COMMITEE.value:
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
        status = UserApplicationStatus(
            name=_next_status,
            updated_by=current_user.id, date=datetime.now(),
        )

    await mobility_svc.add_status(
        db_mongo=db_mongo,
        new_status=status,
        user_application_id=user_application_id,
    )

# Generar documento

# mobility_dict = MobilityResponse.dict()

# mobility_dict = {
#     'date': '23/01/2025',
#     'name': 'Jhon Jaramillo',
#     'phone': '123456789',
#     'email': 'jeronimo@udea.edu.co',
#     'identification_type': 'Cédula de ciudadanía',
#     'identification_number': '987654321',
#     'nationality': 'Colombiana',
#     'rol': 'Estudiante',
#     'school': 'Facultad de Ciencias Exactas y Naturales',
#     'current_academic_program': 'Ingeniería Química',
#     'semester': '8',
#     'name_coordinator': 'Dra. María Pérez',
#     'phone_coordinator': '123456789',
#     'email_coordinator': 'coordinacion@udea.edu.co',
#     'incoming_leaving': 'Saliente',
#     'national_international': 'Internacional',
#     'process': 'Intercambio académico',
#     'destination_country': 'España',
#     'destination_institution': 'Universidad de Barcelona',
#     'academic_program': 'Ingeniería Química',
#     'name_contact_person': 'Dr. Juan López',
#     'cellphone_contact_person': '987654321',
#     'email_contact_person': 'juan.lopez@ub.edu',
#     'date_start': '1 de febrero de 2025',
#     'date_end': '30 de junio de 2025',
#     'signature': 'Jeronimo Pérez',
#     'signature_responsible': 'Dra. Ana Martínez',
#     'date_report': '20 de enero de 2025',

#     'code1': '1234',
#     'subject1': 'Materia 1',
#     'recognized_code1': '1234',
#     'recognized_subject1': 'Materia 1',
#     'code2': '5678',
#     'subject2': 'Materia 2',
#     'recognized_code2': '5678',
#     'recognized_subject2': 'Materia 2',
#     'code3': '9101',
#     'subject3': 'Materia 3',
#     'recognized_code3': '9101',
#     'recognized_subject3': 'Materia 3',
#     'code4': '1121',
#     'subject4': 'Materia 4',
#     'recognized_code4': '1121',
#     'recognized_subject4': 'Materia 4',
# }


def generate_mobility_format(mobility_dict: dict, path: str):
    # Crear documento a partir de una plantilla
    print(mobility_dict['type'])
    print(type(mobility_dict['type']))
    mobility_data = {
        # 'date': mobility_dict['date'],

        'name': mobility_dict['name'] + ' ' + mobility_dict['last_name'],
        'phone': mobility_dict['phone'],
        'email': mobility_dict['email'],
        'identification_type': mobility_dict['identification_type']
        .replace('_', ' '),
        'identification_number': mobility_dict['identification_number'],
        # 'nationality': mobility_dict['nationality'],
        'rol': 'Estudiante',
        # 'school': mobility_dict['school'],
        # 'current_academic_program': mobility_dict[
        # 'current_academic_program'
        # ],
        # 'semester': mobility_dict['semester'],

        # 'name_coordinator': mobility_dict['name_coordinator'],
        # 'phone_coordinator': mobility_dict['phone_coordinator'],
        # 'email_coordinator': mobility_dict['email_coordinator'],

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

        # 'code1': mobility_dict['code1'],
        # 'subject1': mobility_dict['subject1'],
        # 'recognized_code1': mobility_dict['recognized_code1'],
        # 'recognized_subject1': mobility_dict['recognized_subject1'],
        # 'code2': mobility_dict['code2'],
        # 'subject2': mobility_dict['subject2'],
        # 'recognized_code2': mobility_dict['recognized_code2'],
        # 'recognized_subject2': mobility_dict['recognized_subject2'],
        # 'code3': mobility_dict['code3'],
        # 'subject3': mobility_dict['subject3'],
        # 'recognized_code3': mobility_dict['recognized_code3'],
        # 'recognized_subject3': mobility_dict['recognized_subject3'],
        # 'code4': mobility_dict['code4'],
        # 'subject4': mobility_dict['subject4'],
        # 'recognized_code4': mobility_dict['recognized_code4'],
        # 'recognized_subject4': mobility_dict['recognized_subject4'],

        # 'signature': mobility_dict['signature'],
        # 'signature_responsible': mobility_dict['signature_responsible'],

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
        print(f'Archivo eliminado: {file_path}')
    except FileNotFoundError:
        print(f'Archivo no encontrado: {file_path}')
