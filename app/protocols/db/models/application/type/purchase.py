from __future__ import annotations

from enum import Enum


class PurchaseStatus(Enum):
    SENT_TO_ACADEMIC_UNIT = 'Enviado a Unidad Académica'
    ASSISTANT_ASSIGNED = 'Auxiliar Asignado'
    CDP_REQUESTED = 'CDP Solicitado'
    CDP_APPROVED = 'CDP Aprobado'
    UPDATED_DOCUMENTS = 'Documentos Actualizados'
    SELECTED_PROVIDER = 'Proveedor Seleccionado'
    ORDER_PLACED = 'Orden de Compra Realizada'
    FINISHED = 'Finalizado'
    REJECTED = 'Rechazado'
