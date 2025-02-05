from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from uuid import UUID

from odmantic.session import AIOSession
from sqlalchemy.orm import Session

from app.infraestructure.policies.application.user_application import (
    create_voting,
)
from app.infraestructure.policies.application.user_application import (
    current_status,
)
from app.infraestructure.policies.application.user_application import (
    send_to_academic_unit,
)
from app.protocols.db.models.application.application import ApplicationStatusType
from app.schemas.application.user_application import UserApplicationStatus
from app.schemas.users.user import User
from app.services.application.type.commission import commission_svc
from app.services.users.user_rol_academic_unit import (
    user_rol_academic_unit_svc,
)


def next_status(current_status: str, response: str | None = None) -> str | None:
    """
    Determines the next application status based on the current status and optional response.

    Args:
        current_status (str): The current status of the application.
        response (str | None, optional): An optional response value that can influence the status transition.
            - "APROBADA" (Approved) or "RECHAZADA" (Rejected) when the status is APPROVAL or IN_DEAN.
            - Defaults to None if no response is given.

    Returns:
        str | None: The next application status based on the provided transition rules.
            - Returns `None` if no valid transition exists for the given `current_status` or response.

    """
    if current_status == ApplicationStatusType.CREATE.value:
        return ApplicationStatusType.IN_COMMITEE.value
    elif current_status == ApplicationStatusType.IN_COMMITEE.value:
        if (response == 'APROBADA'):
            return ApplicationStatusType.IN_INTERNATIONAL.value
        elif (response == 'RECHAZADA'):
            return ApplicationStatusType.RETURNED.value
        else:
            return ApplicationStatusType.RETURNED.value
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
    start_date: datetime,
    end_date: datetime,
    user_application_id: UUID,
    db_mongo: AIOSession,
    db_postgres: Session,
    current_user: User,
) -> str:
    _current_status = await current_status(
        user_application_id,
        db_mongo,
        commission_svc,
    )

    _next_status = next_status(_current_status)

    if (
        _next_status == ApplicationStatusType.IN_COMMITEE.value and
        (end_date - start_date) >= timedelta(days=30)
    ):

        committees = user_rol_academic_unit_svc.get_by_user_id(
            user_id=current_user.id,
            db=db_postgres,
        )

        for committee in committees:
            send_to_academic_unit(
                academic_unit_id=committee.academic_unit_id,
                user_application_id=user_application_id,
                db=db_postgres,
            )
            # await create_voting(
            #     academic_unit_id=committee.academic_unit_id,
            #     user_application_id=user_application_id,
            #     db_postgres=db_postgres,
            #     db_mongo=db_mongo,
            # )
            status = UserApplicationStatus(
                name=_next_status,
                updated_by=current_user.id,
                date=datetime.now(),
            )
            await commission_svc.add_status(
                db_mongo=db_mongo,
                new_status=status,
                user_application_id=user_application_id,
            )

            return 'terminado'

    else:
        next_status
