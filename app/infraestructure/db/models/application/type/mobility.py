from __future__ import annotations

from datetime import datetime
from uuid import UUID

from odmantic import Field
from odmantic import Model

from app.schemas.application.user_application import UserApplicationStatus


class Mobility(Model):
    id: UUID = Field(primary_field=True)
    process: str
    type: str
    purpose: str
    destination_country: str
    destination_institution: str
    date_start: datetime
    date_end: datetime
    total_time: int
    date_report: datetime
    status: list[UserApplicationStatus]
