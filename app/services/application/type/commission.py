from __future__ import annotations

from app.protocols.db.crud.application.type.commission import CRUDCommissionProtocol
from app.protocols.db.models.application.type.commission import Commission
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.type.commission import CommissionUpdate
from app.services.application.type.base import ApplicationTypeBaseService


class CommissionService(
    ApplicationTypeBaseService[Commission, CommissionCreate,
                               CommissionUpdate, CRUDCommissionProtocol],
):
    """
    Service class for handling Commission-related operations.

    This class is a specialized implementation of the generic ApplicationTypeBaseService.
    It provides business logic and interactions with the database for Commission entities,
    using the CRUDCommissionProtocol for data persistence.

    Generic Parameters:
        - Commission: The model class representing a Commission entity.
        - CommissionCreate: Schema used for creating a new Commission.
        - CommissionUpdate: Schema used for updating an existing Commission.
        - CRUDCommissionProtocol: Protocol defining the database operations for Commission.

    Inherits:
        ApplicationTypeBaseService: Provides base functionality for handling application types.
    """
    ...


commission_svc = CommissionService()
"""
Global instance of CommissionService.

This instance provides access to business logic for Commission entities,
allowing for creation, retrieval, updating, and deletion of Commission records.
"""
