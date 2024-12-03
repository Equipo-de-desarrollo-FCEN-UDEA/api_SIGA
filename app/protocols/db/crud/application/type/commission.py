from __future__ import annotations

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.application.type.commission import Commission
from app.schemas.application.type.commission import CommissionCreate
from app.schemas.application.type.commission import CommissionUpdate


class CRUDCommissionProtocol(CRUDProtocol[Commission, CommissionCreate, CommissionUpdate]):
    ...
