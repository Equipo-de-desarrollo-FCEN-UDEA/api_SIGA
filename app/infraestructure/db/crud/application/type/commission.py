from __future__ import annotations

from app.infraestructure.db.crud.application.type.base import (
    ApplicationTypeBaseCrud,
)
from app.infraestructure.db.models.application.type.commission import (
    Commission,
)
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.type.commission import CommissionUpdate


class CommissionCrud(
    ApplicationTypeBaseCrud[Commission, CommissionCreate, CommissionUpdate],
):
    """
    A specialized CRUD class for managing `Commission` entities.

    This class extends `ApplicationTypeBaseCrud` with the following type
    parameters:
    - `Commission`: The database model representing the `Commission` entity.
    - `CommissionCreate`: The Pydantic schema used for creating new
      commission records.
    - `CommissionUpdate`: The Pydantic schema used for updating existing
      commission records.

    It provides CRUD operations for `Commission` entities, including methods
    for creating, reading, updating, and deleting records in the database.
    """
    ...


commission_crud = CommissionCrud(Commission)
"""
Instance of `CommissionCrud` initialized with the `Commission` model.

This instance can be used for performing CRUD operations specific to the
`Commission` entity. Examples of supported operations include:
- Creating a commission
- Reading commission data by ID
- Updating commission records
- Deleting commission records
"""
