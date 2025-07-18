from __future__ import annotations

from app.protocols.db.crud.organization.academic_unit import CRUDAcademicUnitProtocol
from app.protocols.db.models.organization.academic_unit import AcademicUnit
from app.schemas.organization.academic_unit import AcademicUnitCreate
from app.schemas.organization.academic_unit import AcademicUnitUpdate
from app.services.base import ServiceBase


class AcademicUnitService(
    ServiceBase[
        AcademicUnit,
        AcademicUnitCreate,
        AcademicUnitUpdate,
        CRUDAcademicUnitProtocol,
    ],
):
    ...


academic_unit_svc = AcademicUnitService()
