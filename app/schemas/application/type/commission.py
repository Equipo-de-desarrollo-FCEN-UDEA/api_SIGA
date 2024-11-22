from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Any
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


class CommissionBase(BaseModel):
    id: UUID | None = None
    country: str = Field(max_length=250, min_length=1)
    state: str | None = Field(max_length=250, min_length=1)
    city: str | None = Field(max_length=250, min_length=1)
    date_start: datetime
    date_end: datetime
    reason: str = Field(max_length=500, min_length=5)
    justification: str = Field(max_length=500, min_length=5)
    documents: list[Any] | None


class CommissionCreate(CommissionBase):
    pass


class CommissionUpdate(BaseModel):
    country: str | None = Field(max_length=250, min_length=1)
    state: str | None = Field(max_length=250, min_length=1)
    city: str | None = Field(max_length=250, min_length=1)
    date_start: datetime | None
    date_end: datetime | None
    reason: str | None = Field(max_length=500, min_length=5)
    justification: str | None = Field(max_length=500, min_length=5)
    documents: list[Any] | None


class Compliment(BaseModel):
    documents: list[Any]
    emails: list[str]
    observation: str = Field(max_length=300)


class CommissionInDB(CommissionBase):
    resolution: str | None
    compliment: Compliment | None


class CommissionResponse(CommissionBase):
    commission: CommissionInDB


class CommissionDocument(CommissionInDB):
    @validator('start_date', 'end_date')
    def stringdate(cls, v, values, **kwargs):
        return v.strftime('%A %d de %B del %Y')
