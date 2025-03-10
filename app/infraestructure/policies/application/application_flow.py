from __future__ import annotations

from fastapi import HTTPException

from app.infraestructure.policies.application.user_application import current_status


class ApplicationFlow:
    def __init__(self, status_enum):
        self.status_enum = status_enum
        self.transitions = dict

    async def next(
        self,
        user_application_id, db_mongo, db_postgres, current_user, is_approved=True,
    ):
        _current_status = await current_status(
            user_application_id=user_application_id,
            db_mongo=db_mongo,
            # svc=purchase_svc, esta logica deberá cambiar a la nueva politica de estados
        )

        next_status = self.get_next_status(_current_status, is_approved, current_user)

        if next_status is None:
            raise HTTPException(status_code=400, detail='Invalid transition')

        return await self.transitions[next_status]()

    def get_next_status(self, current_status, is_approved, current_user):
        if not is_approved:
            return self.status_enum.REJECTED

        status_list = list(self.status_enum)
        try:
            index = status_list.index(current_status)
            return status_list[index + 1] if index + 1 < len(status_list) else None
        except ValueError:
            raise HTTPException(status_code=400, detail='Invalid status')

    # Métodos específicos de cada estado
    async def upload_files(self):
        pass  # Implementación específica

    async def assign_user(self):
        pass

    async def complete_information(self):
        pass

    async def request_cdp(self):
        pass

    async def approve_cdp(self):
        pass

    async def update_documents(self):
        pass

    async def select_provider(self):
        pass

    async def place_order(self):
        pass

    async def close(self):
        pass

    async def reject(self):
        pass
