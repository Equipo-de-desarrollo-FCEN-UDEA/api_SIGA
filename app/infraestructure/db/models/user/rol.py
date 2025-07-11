from sqlalchemy import Column, String, Uuid,ForeignKey

from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel

class Rol(BaseModel):
    name = Column(String(100), nullable=False)
    scope = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)

# relations
    user_roles_academic_unit = relationship("UserRolAcademicUnit", back_populates="rol")
