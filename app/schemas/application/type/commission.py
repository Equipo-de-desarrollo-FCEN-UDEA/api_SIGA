from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from app.schemas.application.user_application import UserApplicationStatus


class CommissionBase(BaseModel):
    id: UUID | None = None
    country: str = Field(max_length=250, min_length=1)
    state: str | None = Field(max_length=250, min_length=1)
    city: str | None = Field(max_length=250, min_length=1)
    date_start: datetime
    date_end: datetime
    reason: str = Field(max_length=500, min_length=5)
    justification: str = Field(max_length=500, min_length=5)
    status: list[UserApplicationStatus] = Field(default_factory=list)
    documents: list[Any] = Field(default_factory=list)


class CommissionCreate(CommissionBase):
    ...


class CommissionUpdate(BaseModel):
    country: str | None = Field(max_length=100, min_length=1)
    state: str | None = Field(max_length=100, min_length=1)
    city: str | None = Field(max_length=100, min_length=1)
    date_start: datetime | None
    date_end: datetime | None
    reason: str | None = Field(max_length=100, min_length=5)
    justification: str | None = Field(max_length=250, min_length=5)
    status: list[UserApplicationStatus] = Field(default_factory=list)
    documents: list[Any] | None


class Compliment(BaseModel):
    documents: list[Any] | None
    emails: list[str] | None
    observation: str = Field(max_length=300)


class CommissionInDB(CommissionBase):
    resolution: str | None = None
    compliment: Compliment | None = None


class CommissionResponse(CommissionInDB):
    ...


class CommissionDocument(CommissionInDB):
    @validator('date_start', 'date_end')
    def stringdate(cls, v, values, **kwargs):
        return v.strftime('%A %d de %B del %Y')
