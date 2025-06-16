from __future__ import annotations

from datetime import timedelta

from app.infraestructure.db.models.application.type.commission import Commission
from app.infraestructure.policies.application.application_flow import ApplicationFlow
from app.services.application.type.commission import commission_svc


class CommissionFlow(ApplicationFlow):
    def __init__(self, user_application):
        super().__init__(user_application)

    async def more_than_thirty_days(self, **kwargs):
        commission: Commission = await commission_svc.get(
            id=self.user_application.id,
            db=kwargs.get('db_mongo'),
        )

        date_start = commission.date_start
        date_end = commission.date_end

        if (date_end - date_start) >= timedelta(days=30):
            response = await self.create_voting(**kwargs)

        else:
            response = await self.next_status(
                jump=2,
                **kwargs,
            )
            '''
            jump 2, porque se salta las dos votaciones y pasa por instituto
            '''

        return response

    async def upload_proof(self, **kwargs):

        academic_unit_id = 'adb1ea44-189f-47a7-b763-e0aae6e7c07e'

        kwargs.pop('academic_unit_id', None)
        return await self.send_to_academic_unit_if_not_created_yet(
            academic_unit_id=academic_unit_id,
            **kwargs,
        )
