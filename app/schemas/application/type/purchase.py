from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.protocols.db.models.application.type.purchase import PurchaseScope
from app.protocols.db.models.application.type.purchase import PurchaseType
from app.schemas.application.user_application import UserApplicationStatus


class AnnualPlan(BaseModel):
    is_true: bool = False
    code: str


class BankConsultation(BaseModel):
    is_true: bool = False
    code: str


class PriorConsultation(BaseModel):
    annual_plan: AnnualPlan | None = None
    bank_consultation: BankConsultation | None = None
    contract: str | None = None


class PurchaseBase(BaseModel):
    id: UUID | None = None
    type: PurchaseType
    scope: PurchaseScope
    need: str
    description: str
    responsible_condition: str
    estimated_budget: float
    marco_agreement: bool | None = None
    status: list[UserApplicationStatus] | None = None
    prior_consultation: PriorConsultation | None = None


class PurchaseCreate(PurchaseBase):
    ...


class PurchaseUpdate(BaseModel):
    type: PurchaseType | None = None
    scope: PurchaseScope | None = None
    need: str | None = None
    description: str | None = None
    responsible_condition: str | None = None
    estimated_budget: float | None = None
    marco_agreement: bool | None = None
    status: list[UserApplicationStatus] | None = None
    prior_consultation: list[PriorConsultation] | None = None
