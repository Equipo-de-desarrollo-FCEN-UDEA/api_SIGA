from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.protocols.db.models.application.type.purchase import PurchaseScope
from app.protocols.db.models.application.type.purchase import PurchaseType


class AnnualPlan(BaseModel):
    is_true: bool = False
    code: str | None = None


class BankConsultation(BaseModel):
    is_true: bool = False
    code: str | None = None


class PriorConsultation(BaseModel):
    annual_plan: AnnualPlan | None = None
    bank_consultation: BankConsultation | None = None
    contract: str | None = None


class Provider(BaseModel):
    id: str
    name: str
    phone: str
    email: str


class Material(BaseModel):
    name: str
    quantity: int
    unit_price: float


class PurchaseBase(BaseModel):
    type: PurchaseType
    scope: PurchaseScope
    need: str
    description: str
    estimated_budget: float
    documents: list[str] | None = None


class PurchaseCreate(PurchaseBase):
    id: UUID | None = None


class PurchaseUpdate(BaseModel):
    type: PurchaseType | None = None
    scope: PurchaseScope | None = None
    need: str | None = None
    description: str | None = None
    responsible_condition: str | None = None
    estimated_budget: float | None = None
    marco_agreement: bool | None = None
    prior_consultation: list[PriorConsultation] | None = None
    selected_provider: Provider | None = None
    materials: list[Material] | None = None
    documents: list[str] | None = None


class PurchaseComplete(BaseModel):
    responsible_condition: str | None = None
    marco_agreement: bool | None = None
    prior_consultation: PriorConsultation | None = None


class SelectedProvider(BaseModel):
    selected_provider: Provider
    materials: list[Material]


class PurchasePublic(PurchaseBase, PurchaseComplete):
    selected_provider: Provider | None = None
    materials: list[Material] | None = None

    class Config:
        orm_mode = True
