from __future__ import annotations

from app.protocols.db.crud.application.type.commission import CRUDCommissionProtocol
from app.protocols.db.models.application.type.commission import Commission
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.type.commission import CommissionUpdate
from app.services.application.type.base import ApplicationTypeBaseService


class CommissionService(ApplicationTypeBaseService[Commission, CommissionCreate, CommissionUpdate, CRUDCommissionProtocol]):
    ...


commission_svc = CommissionService()
