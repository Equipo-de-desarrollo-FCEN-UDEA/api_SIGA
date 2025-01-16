from __future__ import annotations

from app.infraestructure.policies.application.user_application import (
    current_status,
)
from app.protocols.db.models.application.application import ApplicationStatusType
from app.schemas.users.user import User
from app.services.application.type.commission import commission_svc


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

    status_transitions = {
        ApplicationStatusType.CREATE.value: ApplicationStatusType.APPROVAL.value,
        ApplicationStatusType.APPROVAL.value: {
            'APROBADA': ApplicationStatusType.IN_DEAN.value,
            'RECHAZADA': ApplicationStatusType.REJECTED.value,
        },
        ApplicationStatusType.IN_DEAN.value: {
            'APROBADA': ApplicationStatusType.APPROVED.value,
            'RECHAZADA': ApplicationStatusType.REJECTED.value,
        },
    }

    if current_status not in status_transitions:
        return None

    if isinstance(status_transitions[current_status], dict) and response:
        return status_transitions[current_status].get(response)

    return status_transitions[current_status]


async def flux(
    *,
    user_application_id,
    db_mongo,
    db_postgres,
    current_user: User,
) -> str:
    _current_status = await current_status(
        user_application_id,
        db_mongo,
        commission_svc,
    )
    _next_status = next_status(_current_status)
