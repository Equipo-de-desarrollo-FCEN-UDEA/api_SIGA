from sqlalchemy import Column, String, Uuid,ForeignKey

from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel

class Rol(BaseModel):
    name = Column(String(100), nullable=False)
    scope = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    academic_unit_id = Column(Uuid,ForeignKey("academic_unit.id") ,nullable=False)

# relations
    academic_unit = relationship("AcademicUnit", back_populates="roles")
    user_roles_academic_unit = relationship("UserRolAcademicUnit", back_populates="rol")

    #users = relationship("User", secondary="user_rol_academic_unit", back_populates="roles")
