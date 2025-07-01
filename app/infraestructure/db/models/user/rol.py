from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel


class Rol(BaseModel):
    name = Column(String(100), nullable=False)
    scope = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    academic_unit_id = Column(Integer, ForeignKey('academic_unit.id'), nullable=False)

# relations
    academic_unit = relationship('AcademicUnit', back_populates='roles')
    user_roles_academic_unit = relationship('UserRolAcademicUnit', back_populates='rol')
