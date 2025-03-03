from __future__ import annotations

from uuid import UUID

from odmantic import Field
from odmantic import Model

from app.schemas.application.type.purchase import PriorConsultation
from app.schemas.application.user_application import UserApplicationStatus


class Provider(Model):
    id: str = Field(primary_field=True)
    name: str
    phone: str
    email: str


class Material(Model):
    id: UUID = Field(primary_field=True)
    name: str
    quantity: int
    unit_price: float


class Purchase(Model):
    id: UUID = Field(primary_field=True)
    type: str
    scope: str
    need: str
    description: str
    responsible_condition: str | None = None
    estimated_budget: float
    marco_agreement: bool | None = None
    status: list[UserApplicationStatus] = []
    prior_consultation: PriorConsultation | None = None
    selected_provider: Provider | None = None
    materials: list[Material] | None = None
