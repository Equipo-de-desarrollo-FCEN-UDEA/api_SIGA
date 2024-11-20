from pydantic import BaseModel
from uuid import UUID

from app.schemas.utils.base_model import GeneralResponse
from app.schemas.organization.academic_unit import AcademicUnit
from app.schemas.application.user_application import UserApplicationInfo
from app.schemas.application.application import Application
from app.schemas.users.user import UserInDB
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
    user_application: UserApplicationInfo
    votes: list[Vote]

    class Config:
        from_attributes = True
