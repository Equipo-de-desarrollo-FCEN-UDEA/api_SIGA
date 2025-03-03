from __future__ import annotations

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.application.type.purchase import Purchase
from app.schemas.application.type.purchase import PurchaseCreate
from app.schemas.application.type.purchase import PurchaseUpdate


class CRUDPurchaseProtocol(CRUDProtocol[Purchase, PurchaseCreate, PurchaseUpdate]):
    pass
