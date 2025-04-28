from __future__ import annotations

from datetime import timedelta

from app.infraestructure.db.models.application.type.commission import Commission
from app.infraestructure.policies.application.application_flow import ApplicationFlow
from app.services.application.type.commission import commission_svc
# from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc
# from app.services.application.user_application_status import (
#     user_application_status_svc,
# )


class CommissionFlow(ApplicationFlow):
    def __init__(self, user_application):
        super().__init__(user_application)

    async def more_than_thirty_days(self, **kwargs):
        # db_postgres = kwargs.get('db_postgres')
        commission: Commission = await commission_svc.get(
            id=self.user_application.id,
            db=kwargs.get('db_mongo'),
        )

        date_start = commission.date_start
        date_end = commission.date_end

        if (date_end - date_start) >= timedelta(days=30):
            response = await self.create_voting(**kwargs)

        else:
            response = await self.send_to_academic_unit(jump=2, **kwargs)
            ''''
            jump 2, porque se salta la votación y el paso por instituto
            y decanatura, y va directo a aprobado
            '''

        return response

# def get_next_status(
#     current_status: str,
#     start_date: datetime | None,
#     end_date: datetime | None,
#     response: str | None = None,
# ) -> str | None:
#     """
#     Determines the next application status based on the current status and optional response.
#     """
#     status_transitions = {
#         ApplicationStatusType.CREATE.value: {
#             'APROBADA': (
#                 ApplicationStatusType.IN_COMMITEE.value
#                 if (end_date - start_date) >= timedelta(days=30)
#                 else ApplicationStatusType.APPROVAL.value
#             ),
#             'RECHAZADA': ApplicationStatusType.REJECTED.value,
#         },
#         ApplicationStatusType.IN_COMMITEE.value: {
#             'APROBADA': ApplicationStatusType.IN_INSTITUTE.value,
#             'RECHAZADA': ApplicationStatusType.REJECTED.value,
#         },
#         ApplicationStatusType.IN_INSTITUTE.value: {
#             'APROBADA': ApplicationStatusType.IN_DEAN.value,
#             'RECHAZADA': ApplicationStatusType.REJECTED.value,
#         },
#         ApplicationStatusType.IN_DEAN.value: {
#             'APROBADA': ApplicationStatusType.APPROVED.value,
#             'RECHAZADA': ApplicationStatusType.REJECTED.value,
#         },
#         ApplicationStatusType.APPROVAL.value: {
#             'APROBADA': ApplicationStatusType.APPROVED.value,
#             'RECHAZADA': ApplicationStatusType.REJECTED.value,
#         },
#     }
#     return (
#         status_transitions.get(current_status, {}).get(response)
#         if isinstance(status_transitions.get(current_status), dict)
#         else status_transitions.get(current_status)
#     )
# def create_user_application_status(name: str, updated_by: UUID) -> UserApplicationStatus:
#     return UserApplicationStatus(
#         name=name,
#         updated_by=updated_by,
#         date=datetime.now(),
#     )
# async def flux(
#     *,
#     start_date: datetime | None,
#     end_date: datetime | None,
#     user_application_id: UUID,
#     db_mongo: AIOSession,
#     db_postgres: Session,
#     current_user: User,
#     response: str | None = None,
# ) -> str:
#     """
#     Handles the status transition flow for a user application.
#     """
#     _current_status = await current_status(
#         user_application_id=user_application_id,
#         db_mongo=db_mongo,
#         svc=commission_svc,
#     )
#     _next_status = get_next_status(
#         current_status=_current_status,
#         start_date=start_date,
#         end_date=end_date,
#         response=response,
#     )
#     status = create_user_application_status(
#         name=_next_status,
#         updated_by=current_user.id,
#     )
#     await commission_svc.add_status(
#         db_mongo=db_mongo,
#         new_status=status,
#         user_application_id=user_application_id,
#     )
#     if _next_status == ApplicationStatusType.IN_COMMITEE.value and (end_date - start_date) >= timedelta(days=30):
#         committees = user_rol_academic_unit_svc.get_by_user_id(
#             user_id=current_user.id, db=db_postgres,
#         )
#         for committee in committees:
#             send_to_academic_unit(
#                 academic_unit_id=committee.academic_unit.academic_unit_id,
#                 user_application_id=user_application_id,
#                 db=db_postgres,
#             )
#             await create_voting(
#                 academic_unit_id=committee.academic_unit.academic_unit_id,
#                 user_application_id=user_application_id,
#                 db_postgres=db_postgres,
#                 db_mongo=db_mongo,
#             )
#         return 'terminado'
#     return 'actualizado'
# from __future__ import annotations
