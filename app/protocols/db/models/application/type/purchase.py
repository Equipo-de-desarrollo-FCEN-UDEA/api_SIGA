from __future__ import annotations

from datetime import datetime
from enum import Enum

from app.protocols.db.utils.mongo_model import MongoModel


class PurchaseType(Enum):
    SMALL = 'Menor cuantía'
    MEDIUM = 'Mediana cuantía'
    LARGE = 'Mayor cuantía'


class PurchaseScope(Enum):
    NATIONAL = 'Nacional'
    INTERNATIONAL = 'Internacional'


class Status():
    name: str
    updated_by: str
    date: datetime


class AnnualPlan():
    is_true: bool = False
    code: str


class BankConsultation():
    is_true: bool = False
    code: str


class PriorConsultation():
    annual_plan: list[AnnualPlan]
    bank_consultation: list[BankConsultation]


class Purchase(MongoModel):
    type: PurchaseType
    scope: PurchaseScope
    need: str
    description: str
    responsible_condition: str
    estimated_budget: float
    marco_agreement: bool | None
    status: list[Status]
    prior_consultation: list[PriorConsultation]


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
