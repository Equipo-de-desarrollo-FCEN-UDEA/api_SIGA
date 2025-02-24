from __future__ import annotations

from datetime import datetime
from enum import Enum

from app.core.config import settings
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
    annual_plan: AnnualPlan
    bank_consultation: BankConsultation
    contract: str


class Purchase(MongoModel):
    type: PurchaseType
    scope: PurchaseScope
    need: str
    description: str
    responsible_condition: str
    estimated_budget: float
    marco_agreement: bool | None
    status: list[Status]
    prior_consultation: PriorConsultation


class PurchaseStatus(Enum):
    CREATED = 'CREADA'
    SENT_TO_ACADEMIC_UNIT = 'Enviado a Unidad Académica'
    ASSISTANT_ASSIGNED = 'Auxiliar Asignado'
    COMPLETED_INFORMATION = 'Información Completada'
    CDP_REQUESTED = 'CDP Solicitado'
    CDP_APPROVED = 'CDP Aprobado'
    UPDATED_DOCUMENTS = 'Documentos Actualizados'
    SELECTED_PROVIDER = 'Proveedor Seleccionado'
    ORDER_PLACED = 'Orden de Compra Realizada'
    FINISHED = 'Finalizado'
    REJECTED = 'Rechazado'


class ApprovedAcademicsUnits(Enum):
    EXTENSION = settings.EXTENSION_ID
    CIEN = settings.CIEN_ID
    FCEN = settings.FCEN
