from __future__ import annotations

import enum

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel

# Definir el enum para identification_type


class IdentificationType(enum.Enum):
    PASAPORTE = 'PASAPORTE'
    TARJETA_DE_IDENTIDAD = 'TARJETA_DE_IDENTIDAD'
    CEDULA_CIUDADANIA = 'CEDULA_CIUDADANIA'
    CEDULA_EXTRANJERIA = 'CEDULA_EXTRANJERIA'


class User(BaseModel):
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    identification_type = Column(Enum(IdentificationType), nullable=False)
    identification_number = Column(String(50), unique=True)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(300), nullable=False)
    is_active = Column(Boolean, nullable=True, default=False)

    # # relations
    user_roles_academic_units = relationship(
        'UserRolAcademicUnit', back_populates='user', lazy='joined',
    )
    user_applications = relationship('UserApplication', back_populates='user')
    votes = relationship('Vote', back_populates='user')
    user_applications_user = relationship(
        'UserApplicationUser', back_populates='user', lazy='joined',
    )

    user_application_status = relationship(
        'UserApplicationStatus', back_populates='user',
    )
