from __future__ import annotations

from app.protocols.db.models.application.type.shoping import ShopingStatus


def next_status(*, current_status: str, is_approved: bool = False) -> str:
    status_list = list(ShopingStatus)
    if is_approved:
        for i, status in enumerate(status_list):
            if status.value == current_status:
                if i+1 < len(status_list):
                    return status_list[i+1]
    return ShopingStatus.REJECTED
