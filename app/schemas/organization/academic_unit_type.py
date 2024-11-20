from pydantic import BaseModel
from uuid import UUID
from app.schemas.utils.base_model import GeneralResponse

class AcademicUnitTypeBase(BaseModel):
    name: str

class AcademicUnitTypeCreate(AcademicUnitTypeBase):
    ...

class AcademicUnitTypeUpdate(BaseModel):
    name: str | None

class AcademicUnitTypeInDB(GeneralResponse, AcademicUnitTypeBase):
    ...

class AcademicUnitType(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True