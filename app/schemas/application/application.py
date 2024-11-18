from pydantic import BaseModel
from uuid import UUID

from app.schemas.utils.base_model import GeneralResponse

class ApplicationBase(BaseModel):
    name: str
    description: str
    academic_unit_id: UUID

    class config:
        from_attributes = True

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    name: str | None
    description: str | None
    academic_unit_id: UUID | None

class Application(ApplicationBase):
    id: UUID

    class Config:
        from_attributes = True


