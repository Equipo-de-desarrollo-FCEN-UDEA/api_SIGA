from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.application.application_status import (
    ApplicationStatus,
)
from app.schemas.application.application_status import ApplicationStatusCreate
from app.schemas.application.application_status import ApplicationStatusUpdate


class ApplicationStatusCrud(
    CRUDBase[
        ApplicationStatus,
        ApplicationStatusCreate,
        ApplicationStatusUpdate,
    ],
):

    def get_next_step(self, current_step, application_id, db: Session) -> str:
        with db:
            response = db.query(ApplicationStatus).filter(
                ApplicationStatus.application_id == application_id,
                ApplicationStatus.step == current_step+1,
            ).first()

            if not response:
                raise HTTPException(
                    status_code=404,
                    detail='Next step not found',
                )
            return response.status.description


application_status_crud = ApplicationStatusCrud(ApplicationStatus)
