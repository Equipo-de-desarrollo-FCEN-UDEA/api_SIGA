from __future__ import annotations

from uuid import UUID

from app.errors.base import BaseErrors
from app.protocols.db.crud.application.user_application_academic_unit import (
    CRUDUserApplicationAcademicUnitProtocol,
)
from app.protocols.db.models.application.user_application_academic_unit import (
    UserApplicationAcademicUnit,
)
from app.schemas.application.user_application_academic_unit import (
    UserApplicationAcademicUnitCreate,
)
from app.schemas.application.user_application_academic_unit import (
    UserApplicationAcademicUnitUpdate,
)
from app.services.base import ServiceBase

NOT_AVAILABLE = 'Service not available'


class UserApplicationAcademicUnitService(
    ServiceBase[
        UserApplicationAcademicUnit,
        UserApplicationAcademicUnitCreate,
        UserApplicationAcademicUnitUpdate,
        CRUDUserApplicationAcademicUnitProtocol,
    ],
):
    def get_by_academic_unit(
            self,
            *,
            academic_unit_id: UUID,
            db,
    ) -> UserApplicationAcademicUnit:
        if self.observer is None:
            raise BaseErrors(
                code=503,
                detail=NOT_AVAILABLE,
            )
        return self.observer.get_by_academic_unit(
            academic_unit_id=academic_unit_id, db=db,
        )

    def get_active(
            self,
            *,
            user_application_id: UUID,
            db,
    ) -> UserApplicationAcademicUnit:
        if self.observer is None:
            raise BaseErrors(
                code=503,
                detail=NOT_AVAILABLE,
            )
        return self.observer.get_active(
            user_application_id=user_application_id,
            db=db,
        )

    def response(
            self,
            *,
            user_application_id: UUID,
            academic_unit_id: UUID,
            db,
    ) -> UserApplicationAcademicUnit:
        if self.observer is None:
            raise BaseErrors(
                code=503,
                detail=NOT_AVAILABLE,
            )
        return self.observer.response(
            user_application_id=user_application_id,
            academic_unit_id=academic_unit_id, db=db,
        )


user_application_academic_unit_svc = UserApplicationAcademicUnitService()
