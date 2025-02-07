from __future__ import annotations

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.application.type.commission import Commission
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.type.commission import CommissionUpdate


class CRUDCommissionProtocol(CRUDProtocol[Commission, CommissionCreate, CommissionUpdate]):
    """
    Protocol defining the CRUD operations for Commission entities.

    This class extends the generic CRUDProtocol to specialize it for the Commission model,
    using the following type parameters:

    Generic Parameters:
        - Commission: The model representing a Commission entity.
        - CommissionCreate: The schema defining the structure for creating a new Commission.
        - CommissionUpdate: The schema defining the structure for updating an existing Commission.

    Inherits:
        CRUDProtocol: A generic protocol defining base CRUD operations such as create, read, update, and delete.

    Purpose:
        - Defines the interface for interacting with the database layer specific to Commission entities.
        - Ensures that the service and repository layers adhere to a consistent contract for database operations.

    Example Usage:
        - This protocol would typically be implemented by a repository class that interacts with the database.
    """
    ...
