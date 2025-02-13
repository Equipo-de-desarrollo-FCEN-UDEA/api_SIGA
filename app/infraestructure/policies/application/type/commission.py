from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from uuid import UUID

from odmantic.session import AIOSession
from sqlalchemy.orm import Session

from app.infraestructure.policies.application.user_application import create_voting
from app.infraestructure.policies.application.user_application import current_status
from app.infraestructure.policies.application.user_application import send_to_academic_unit
from app.protocols.db.models.application.application import ApplicationStatusType
from app.schemas.application.user_application import UserApplicationStatus
from app.schemas.users.user import User
from app.services.application.type.commission import commission_svc
from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc


def get_next_status(
    current_status: str,
    start_date: datetime,
    end_date: datetime,
    response: str | None = None,
) -> str | None:
    """
    Determines the next application status based on the current status and optional response.
    """
    status_transitions = {
        ApplicationStatusType.CREATE.value: {
            'APROBADA': (
                ApplicationStatusType.IN_COMMITEE.value
                if (end_date - start_date) >= timedelta(days=30)
                else ApplicationStatusType.APPROVAL.value
            ),
            'RECHAZADA': ApplicationStatusType.REJECTED.value,
        },
        ApplicationStatusType.IN_COMMITEE.value: {
            'APROBADA': ApplicationStatusType.IN_INSTITUTE.value,
            'RECHAZADA': ApplicationStatusType.REJECTED.value,
        },
        ApplicationStatusType.IN_INSTITUTE.value: {
            'APROBADA': ApplicationStatusType.IN_DEAN.value,
            'RECHAZADA': ApplicationStatusType.REJECTED.value,
        },
        ApplicationStatusType.IN_DEAN.value: {
            'APROBADA': ApplicationStatusType.APPROVED.value,
            'RECHAZADA': ApplicationStatusType.REJECTED.value,
        },
        ApplicationStatusType.APPROVAL.value: {
            'APROBADA': ApplicationStatusType.APPROVED.value,
            'RECHAZADA': ApplicationStatusType.REJECTED.value,
        },
    }
    return (
        status_transitions.get(current_status, {}).get(response)
        if isinstance(status_transitions.get(current_status), dict)
        else status_transitions.get(current_status)
    )


def create_user_application_status(name: str, updated_by: UUID) -> UserApplicationStatus:
    return UserApplicationStatus(
        name=name,
        updated_by=updated_by,
        date=datetime.now(),
    )


async def flux(
    *,
    start_date: datetime,
    end_date: datetime,
    user_application_id: UUID,
    db_mongo: AIOSession,
    db_postgres: Session,
    current_user: User,
    response: str | None = None,
) -> str:
    """
    Handles the status transition flow for a user application.
    """
    _current_status = await current_status(
        user_application_id=user_application_id,
        db_mongo=db_mongo,
        svc=commission_svc,
    )

    _next_status = get_next_status(
        current_status=_current_status,
        start_date=start_date,
        end_date=end_date,
        response=response,
    )

    status = create_user_application_status(
        name=_next_status,
        updated_by=current_user.id,
    )

    await commission_svc.add_status(
        db_mongo=db_mongo,
        new_status=status,
        user_application_id=user_application_id,
    )

    if _next_status == ApplicationStatusType.IN_COMMITEE.value and (end_date - start_date) >= timedelta(days=30):
        committees = user_rol_academic_unit_svc.get_by_user_id(
            user_id=current_user.id, db=db_postgres,
        )

        for committee in committees:

            send_to_academic_unit(
                academic_unit_id=committee.academic_unit.academic_unit_id,
                user_application_id=user_application_id,
                db=db_postgres,
            )

            await create_voting(
                academic_unit_id=committee.academic_unit.academic_unit_id,
                user_application_id=user_application_id,
                db_postgres=db_postgres,
                db_mongo=db_mongo,
            )

        return 'terminado'

    return 'actualizado'
