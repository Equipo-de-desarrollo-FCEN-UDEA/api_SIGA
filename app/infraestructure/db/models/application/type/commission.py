from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from odmantic import Field
from odmantic import Model

from app.schemas.application.user_application import UserApplicationStatus


class Commission(Model):
    id: UUID = Field(primary_field=True)
    country: str
    state: str | None
    city: str | None
    date_start: datetime
    date_end: datetime
    reason: str
    justification: str
    documents: list[Any] | None
    resolution: str | None
    compliment: Any | None
    status: list[UserApplicationStatus]
