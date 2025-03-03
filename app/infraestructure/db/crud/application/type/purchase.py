from __future__ import annotations

from app.infraestructure.db.crud.application.type.base import (
    ApplicationTypeBaseCrud,
)
from app.infraestructure.db.models.application.type.purchase import Purchase
from app.schemas.application.type.purchase import PurchaseCreate
from app.schemas.application.type.purchase import PurchaseUpdate


class PurchaseCrud(
    ApplicationTypeBaseCrud[Purchase, PurchaseCreate, PurchaseUpdate],
):
    pass


purchase_crud = PurchaseCrud(Purchase)
