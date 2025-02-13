from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.schemas.application.user_application import UserApplicationInfo
from app.schemas.utils.base_model import GeneralResponse
from app.schemas.voting.vote import Vote


class VotingBase(BaseModel):
    academic_unit_id: UUID
    user_application_id: UUID


class VotingCreate(VotingBase):
    pass


class VotingUpdate(BaseModel):
    academic_unit_id: UUID | None
    user_application_id: UUID | None


class VotingInDB(VotingBase):
    id: UUID


class VotingResponse(GeneralResponse):
    academic_unit_id: UUID
    user_application: UserApplicationInfo
    votes: list[Vote]

    class Config:
        from_attributes = True
