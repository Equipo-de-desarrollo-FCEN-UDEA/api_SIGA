from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.infraestructure.policies.application.user_application import current_status
from app.infraestructure.policies.application.user_application import (
    send_to_academic_unit,
)
from app.infraestructure.policies.application.user_application import send_to_user
from app.protocols.db.models.application.type.purchase import PurchaseStatus
from app.schemas.application.type.purchase import PurchaseUpdate
from app.schemas.application.user_application import UserApplicationStatus
from app.schemas.users.user import User
from app.services.application.type.purchase import purchase_svc

STATUS_LIST = list(PurchaseStatus)


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


async def flux(
        *,
        user_application_id,
        db_mongo,
        db_postgres,
        current_user: User,
        is_approved: bool | None = None,
        user_to_assign: UUID | None = None,
        academic_unit_id: UUID | None = None,
        obj_in: PurchaseUpdate | None = None,
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
        pass

    def select_provider():
        pass

    def place_order():
        pass

    def close():
        pass

    def reject():
        pass

    if _current_status == PurchaseStatus.CREATED.value:
        res = send_to_academic_unit(
            user_application_id=user_application_id,
            academic_unit_id=academic_unit_id,
            db=db_postgres,
        )

    elif _current_status == PurchaseStatus.SENT_TO_ACADEMIC_UNIT.value:
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

    await purchase_svc.add_status(
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        new_status=_next_status,
        user_application_id=user_application_id,
    )
    return res
