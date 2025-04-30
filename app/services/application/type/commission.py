from __future__ import annotations

from app.protocols.db.crud.application.type.commission import CRUDCommissionProtocol
from app.protocols.db.models.application.type.commission import Commission
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.type.commission import CommissionUpdate
from app.services.base import ServiceBase


class CommissionService(
    ServiceBase[
        Commission,
        CommissionCreate,
        CommissionUpdate,
        CRUDCommissionProtocol,
    ],
):
    pass


commission_svc = CommissionService()
"""
Global instance of CommissionService.

This instance provides access to business logic for Commission entities,
allowing for creation, retrieval, updating, and deletion of Commission records.
"""
