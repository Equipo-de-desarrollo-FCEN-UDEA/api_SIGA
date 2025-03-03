from __future__ import annotations

import os
from datetime import datetime
from tempfile import NamedTemporaryFile
from uuid import UUID

from docx import Document
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.infraestructure.policies.application.user_application import current_status
from app.infraestructure.policies.application.user_application import send_to_user
from app.infraestructure.services.aws.s3 import s3
from app.protocols.db.models.application.type.purchase import PurchaseStatus
from app.schemas.application.type.purchase import Material
from app.schemas.application.type.purchase import Provider
from app.schemas.application.type.purchase import PurchaseUpdate
from app.schemas.application.user_application import UserApplicationStatus
from app.schemas.users.user import User
from app.services.application.type.purchase import purchase_svc
from app.services.application.user_application import user_application_svc

STATUS_LIST = list(PurchaseStatus)
APPLICATION_PDF = 'application/pdf'


def next_status(
        *,
        current_status: str,
        is_approved: bool = True,
        current_user,
) -> UserApplicationStatus:
    if not is_approved:
        name = PurchaseStatus.REJECTED.value
        status = UserApplicationStatus(
            name=name,
            updated_by=current_user.id,
            date=datetime.now(),
        )
        return status
    for i, status in enumerate(STATUS_LIST):
        if status.value == current_status:
            if i+1 < len(STATUS_LIST):
                name = STATUS_LIST[i+1].value
                status = UserApplicationStatus(
                    name=name,
                    updated_by=current_user.id,
                    date=datetime.now(),
                )
                return status
            raise HTTPException(status_code=400, detail='Invalid status')
    raise HTTPException(status_code=400, detail='status not found')


async def flux(
        *,
        user_application_id,
        db_mongo,
        db_postgres,
        current_user: User,
        is_approved: bool | None = None,
        user_to_assign: UUID | None = None,
        obj_in: PurchaseUpdate | None = None,
        files: list[UploadFile] | None = None,
        **kwargs,
) -> JSONResponse:
    _current_status = await current_status(
        user_application_id=user_application_id,
        db_mongo=db_mongo,
        svc=purchase_svc,
    )
    _next_status = next_status(
        current_status=_current_status,
        is_approved=is_approved,
        current_user=current_user,
    )

    res = None

    async def upload_files():
        user_id = user_application_svc.get(
            id=user_application_id,
            db=db_postgres,
        ).user_id
        DIR = f'{str(user_id)}/{str(user_application_id)}/'

        for i, pdf in enumerate(files):
            file_path = f'{DIR}precotizacion-{i}.pdf'
            res = s3.push_data_to_s3_bucket(
                bucket_name=settings.aws_bucket_name,
                data=pdf.file,
                file_name=file_path,
                content_type=APPLICATION_PDF,
            )
        return res

    async def complete_information():
        await purchase_svc.update(
            id=user_application_id,
            obj_in=obj_in,
            db_mongo=db_mongo,
        )
        return JSONResponse(
            status_code=200,
            content={'message': 'Information completed'},
        )

    def request_cdp():
        return JSONResponse(
            status_code=200,
            content={'message': 'CDP requested'},
        )

    def approve_cdp():
        return JSONResponse(
            status_code=200,
            content={'message': 'CDP approved'},
        )

    def update_documents():
        user_id = user_application_svc.get(
            id=user_application_id,
            db=db_postgres,
        ).user_id
        DIR = f'{str(user_id)}/{str(user_application_id)}/'

        for i, pdf in enumerate(files[:-1]):
            file_path = f'{DIR}cotizacion-{i}.pdf'
            s3.push_data_to_s3_bucket(
                bucket_name=settings.aws_bucket_name,
                data=pdf.file,
                file_name=file_path,
                content_type=APPLICATION_PDF,
            )
        res = s3.push_data_to_s3_bucket(
            bucket_name=settings.aws_bucket_name,
            data=files[-1].file,
            file_name=f'{DIR}cuadro-comparativo.pdf',
            content_type=APPLICATION_PDF,
        )
        return res

    async def select_provider():
        provider: Material = kwargs.get('provider')
        materials: Provider = kwargs.get('materials')

        if not provider or not materials:
            raise HTTPException(
                status_code=400, detail='Provider and materials are required',
            )

        purchase_update = PurchaseUpdate(
            selected_provider=provider,
            materials=materials,
        )
        await purchase_svc.update(
            id=user_application_id,
            obj_in=purchase_update,
            db_mongo=db_mongo,
        )
        return JSONResponse(
            status_code=200,
            content={'message': 'Provider selected'},
        )

    def place_order():
        pass

    def close():
        pass

    def reject():
        pass

    if _current_status == PurchaseStatus.CREATED.value:
        res = await upload_files()

    elif _current_status == PurchaseStatus.UPLOADED_FILES.value:
        res = send_to_user(
            user_application_id=user_application_id,
            user_id=user_to_assign,
            db=db_postgres,
        )

    elif _current_status == PurchaseStatus.ASSISTANT_ASSIGNED.value:
        res = await complete_information()

    elif _current_status == PurchaseStatus.COMPLETED_INFORMATION.value:
        res = request_cdp()

    elif _current_status == PurchaseStatus.CDP_REQUESTED.value:
        res = approve_cdp()

    elif _current_status == PurchaseStatus.CDP_APPROVED.value:
        res = update_documents()

    elif _current_status == PurchaseStatus.UPDATED_DOCUMENTS.value:
        res = await select_provider()

    if res is None:
        raise HTTPException(status_code=400, detail='Invalid status')

    await purchase_svc.add_status(
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        new_status=_next_status,
        user_application_id=user_application_id,
    )
    return res


def generate_format(purchase_dict: dict, path: str):
  
    purchase_data = {
        'date': f"{purchase_dict['status'][0].date.strftime('%Y-%m-%d')}",
        'academic_unit': str(purchase_dict.get('academic_unit', '')),
        'cost_center': '',
        'need': str(purchase_dict.get('need', '')),
        'description': str(purchase_dict.get('description', '')),
        'estimated_budget': str(purchase_dict.get('estimated_budget', '')),
        'marco_yes': '☒' if purchase_dict.get('marco_agreement') else '☐',
        'marco_no': '☒' if purchase_dict.get('marco_agreement') is False else '☐',
        'annual_plan': (
            '☒' if (
                hasattr(
                    purchase_dict.get(
                        'prior_consultation', None,
                    ), 'annual_plan',
                )
                and purchase_dict[
                    'prior_consultation'
                ].annual_plan.is_true
            ) else '☐'
        ),
        'code_annual_plan': (
            str(purchase_dict['prior_consultation'].annual_plan.code)
            if hasattr(
                purchase_dict.get(
                    'prior_consultation', None,
                ), 'annual_plan',
            )
            else ''
        ),
        'bank_consultation': (
            '☒' if (
                hasattr(
                    purchase_dict.get(
                        'prior_consultation', None,
                    ), 'bank_consultation',
                )
                and purchase_dict[
                    'prior_consultation'
                ].bank_consultation.is_true
            ) else '☐'
        ),
        'code_bank_consultation': (
            str(
                purchase_dict[
                    'prior_consultation'
                ].bank_consultation.code,
            )
            if hasattr(
                purchase_dict.get(
                    'prior_consultation', None,
                ), 'bank_consultation',
            )
            else ''
        ),
        'contract': (
            str(
                purchase_dict[
                    'prior_consultation'
                ].contract,
            )
            if hasattr(
                purchase_dict.get(
                    'prior_consultation', None,
                ), 'contract',
            )
            else ''
        ),
        'signature': '',
        'signature_delegate': '',
    }

    try:
        document = Document(path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Error al cargar la plantilla: {str(e)}',
        )

    for paragraph in document.paragraphs:
        for key, value in purchase_data.items():
            if f'{{{{{key}}}}}' in paragraph.text:
                paragraph.text = paragraph.text.replace(
                    f'{{{{{key}}}}}', value,
                )

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in purchase_data.items():
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
