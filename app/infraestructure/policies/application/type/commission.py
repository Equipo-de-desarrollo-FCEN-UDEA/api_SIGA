from __future__ import annotations

from datetime import datetime
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

    async def compliment(self, **kwargs):
        commission: Commission = await commission_svc.get(
            id=self.user_application.id,
            db=kwargs.get('db_mongo'),
        )
        await self.next_status(**kwargs)

        is_approved = kwargs.get('is_approved')
        if is_approved:
            await self.refresh_user_application_state(**kwargs)

            if commission.date_end < datetime.now():
                response = await self.next_status(**kwargs)
                return response

        return None
