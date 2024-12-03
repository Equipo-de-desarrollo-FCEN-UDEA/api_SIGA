from __future__ import annotations

from fastapi import status

from ..base import BaseErrors


class CommissionErrors(BaseErrors):
    ...


COMMISSION_COMPLIMENT_403 = CommissionErrors(
    status.HTTP_403_FORBIDDEN, 'No puedes cumplir tu propia comisión',
)
COMMISSION_COMPLIMENT_409 = CommissionErrors(
    status.HTTP_409_CONFLICT, 'No se puede subir nuevamente un cumplido',
)
