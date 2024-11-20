from sqlalchemy import Column, Uuid, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.link_model import LinkModel

class UserRolAcademicUnit(LinkModel):
    user_id = Column(Uuid, ForeignKey("user.id"), primary_key=True)
    rol_id = Column(Uuid, ForeignKey("rol.id"), primary_key=True)
    academic_unit_id = Column(Uuid, ForeignKey("academic_unit.id"), primary_key=True)
    is_active = Column(Boolean, nullable=False, default=True)

    # user = relationship("User", back_populates="user_roles")
    user = relationship("User", back_populates="user_roles_academic_units")
    rol = relationship("Rol", back_populates="user_roles_academic_unit", lazy="selectin")
    academic_unit = relationship("AcademicUnit", back_populates="user_rol_academic_units")
