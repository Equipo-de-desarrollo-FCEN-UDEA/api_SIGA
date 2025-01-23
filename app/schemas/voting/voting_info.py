from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class VotingStatus(BaseModel):
    result: str
    date: datetime
    observation: str | None = None


class VotingInfoBase(BaseModel):
    id: UUID | None
    statuses: list[VotingStatus] | None = []


class VotingInfoCreate(VotingInfoBase):
    pass


class VotingInfoUpdate(BaseModel):
    statuses: list[VotingStatus] | None = []

    


class VotingInfo(VotingInfoBase):
    pass
