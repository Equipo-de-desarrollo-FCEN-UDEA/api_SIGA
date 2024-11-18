from pydantic import BaseModel
from uuid import UUID

from app.schemas.utils.base_model import GeneralResponse

class VoteTypeBase(BaseModel):
    name: str
    description: str

class VoteTypeCreate(VoteTypeBase):
    pass

class VoteTypeUpdate(BaseModel):
    name: str | None
    description: str | None

class VoteTypeInDB(VoteTypeBase):
    id: UUID

class VoteType(BaseModel):
    name: str

    class Config:
        from_attributes = True
