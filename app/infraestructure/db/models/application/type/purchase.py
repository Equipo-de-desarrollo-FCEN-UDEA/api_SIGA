from __future__ import annotations

from uuid import UUID

from odmantic import Field
from odmantic import Model

from app.schemas.application.type.purchase import PriorConsultation
from app.schemas.application.user_application import UserApplicationStatus


class Purchase(Model):
    id: UUID = Field(primary_field=True)
    type: str
    scope: str
    need: str
    description: str
    responsible_condition: str
    estimated_budget: float
    marco_agreement: bool
    status: list[UserApplicationStatus]
    prior_consultation: PriorConsultation
