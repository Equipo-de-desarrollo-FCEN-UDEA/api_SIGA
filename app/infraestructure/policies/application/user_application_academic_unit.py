from __future__ import annotations

from app.infraestructure.db.models.application.user_application_academic_unit import (
    UserApplicationAcademicUnit,
)
from app.infraestructure.policies.application.type import mobility
from app.protocols.db.models.application.user_application_academic_unit import Result


async def response(
        user_application_academic_unit: UserApplicationAcademicUnit,
        *,
        db_mongo,
        db_postgres,
        current_user,
        result,
):

    user_application = user_application_academic_unit.user_application
    aplication = user_application.application
    application_type = aplication.name
    if result == Result.APPROVED:
        response = 'APROBADA'
    response = 'RECHAZADA'
    if application_type == 'MOVILIDAD':
        await mobility.flux(
            user_application_id=user_application.id,
            db_mongo=db_mongo,
            db_postgres=db_postgres,
            current_user=current_user,
            response=response,
        )
