from __future__ import annotations

from app.protocols.db.crud.application.type.purchase import CRUDPurchaseProtocol
from app.protocols.db.models.application.type.purchase import Purchase
from app.schemas.application.type.purchase import PurchaseCreate
from app.schemas.application.type.purchase import PurchaseUpdate
from app.services.application.type.base import ApplicationTypeBaseService


class PurchaseService(
    ApplicationTypeBaseService[
        Purchase,
        PurchaseCreate,
        PurchaseUpdate,
        CRUDPurchaseProtocol,
    ],
):
    pass


purchase_svc = PurchaseService()
