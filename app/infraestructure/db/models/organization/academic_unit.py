from sqlalchemy import Column, Uuid, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel

class AcademicUnit(BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(100))

    academic_unit_id = Column(Uuid, ForeignKey("academic_unit.id"), nullable=True)
    academic_unit_type_id = Column(Uuid, ForeignKey("academic_unit_type.id"), nullable=True)

    # relations    
    academic_unit = relationship("AcademicUnit", remote_side="AcademicUnit.id" ,back_populates="academic_units", lazy="joined")
    academic_unit_type = relationship("AcademicUnitType", back_populates="academic_units" , lazy="selectin")
    
    roles = relationship("Rol", back_populates="academic_unit")

    academic_units = relationship("AcademicUnit", back_populates="academic_unit", cascade="all, delete-orphan", lazy="joined")

    user_rol_academic_units = relationship("UserRolAcademicUnit", back_populates="academic_unit")

    applications = relationship("Application", back_populates="academic_unit")
    user_application_academic_units = relationship("UserApplicationAcademicUnit", back_populates="academic_unit")

    votings = relationship("Voting", back_populates="academic_unit")
    