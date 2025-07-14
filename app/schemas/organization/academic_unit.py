from pydantic import BaseModel
from uuid import UUID

from app.schemas.utils.base_model import GeneralResponse
from app.schemas.organization.academic_unit_type import AcademicUnitTypeInDB, AcademicUnitType

class AcademicUnitBase(BaseModel):
    name:str
    email: str
    academic_unit_id: UUID | None = None
    academic_unit_type_id: UUID
    
class AcademicUnitCreate(AcademicUnitBase):
    ...
    
class AcademicUnitUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    academic_unit_id: UUID | None = None
    academic_unit_type_id: UUID | None = None
    
class AcademicUnitInDB(GeneralResponse, AcademicUnitBase):
    ...

class AcademicUnit(BaseModel):
    id: UUID
    name: str
    academic_unit_type: AcademicUnitType
    
    class Config:
        orm_mode = True
        from_attributes = True

class program(AcademicUnit):
    pass

class Institute(AcademicUnit):
    academic_units: list[program]

class School(AcademicUnit):
    academic_units: list[Institute]
    

