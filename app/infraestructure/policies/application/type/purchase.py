from __future__ import annotations

from app.protocols.db.models.application.type.purchase import PurchaseStatus


def next_status(*, current_status: str, is_approved: bool = False) -> PurchaseStatus:
    status_list = list(PurchaseStatus)
    if is_approved:
        for i, status in enumerate(status_list):
            if status.value == current_status:
                if i+1 < len(status_list):
                    return status_list[i+1]
    return PurchaseStatus.REJECTED
