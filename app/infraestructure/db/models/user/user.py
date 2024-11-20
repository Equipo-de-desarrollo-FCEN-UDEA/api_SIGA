from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from app.infraestructure.db.utils.base_model import BaseModel

import enum 

if TYPE_CHECKING:
    from app.infraestructure.db.models.user.rol import Rol

# Definir el enum para identification_type
class IdentificationType(enum.Enum):
    PASAPORTE = "pasaporte"
    TARJETA_DE_IDENTIDAD = "tarjeta_de_identidad"
    CEDULA_CIUDADANIA = "cedula_ciudadania"
    CEDULA_EXTRANJERIA = "cedula_extranjeria"


class User(BaseModel):
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    identification_type= Column(Enum(IdentificationType), nullable=False)
    identification_number= Column(String(50), unique=True)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(300), nullable=False)
    is_active = Column(Boolean, nullable=True, default=True)



    # # relations
    user_roles_academic_units = relationship("UserRolAcademicUnit", back_populates="user", lazy="selectin")
    user_applications = relationship("UserApplication", back_populates="user")
    votes = relationship("Vote", back_populates="user")
    