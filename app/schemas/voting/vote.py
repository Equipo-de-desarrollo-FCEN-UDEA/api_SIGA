from pydantic import BaseModel
from uuid import UUID

from app.schemas.utils.base_model import GeneralResponse
from app.schemas.voting.vote_type import VoteType

class VoteBase(BaseModel):
    voting_id: UUID
    user_id: UUID
    vote_type_id: UUID

class VoteCreate(BaseModel):
    voting_id: UUID
    user_id: UUID | None = None
    vote_type_id: UUID

class VoteUpdate(BaseModel):
    voting_id: UUID | None
    user_id: UUID | None
    vote_type_id: UUID | None

class Vote(BaseModel):
    vote_type: VoteType

    class Config:
        from_attributes = True