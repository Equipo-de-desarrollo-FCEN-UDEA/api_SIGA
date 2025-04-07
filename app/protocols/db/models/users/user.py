from __future__ import annotations

from enum import Enum
from uuid import UUID

from app.protocols.db.utils.base_model import BaseModel

# Definir el enum para identification_type


class IdentificationType(Enum):
    CEDULA_CIUDADANIA = 1
    CEDULA_EXTRANJERIA = 2
    PASAPORTE = 3
    TARJETA_DE_IDENTIDAD = 4


class User(BaseModel):
    id: UUID
    name: str
    last_name: str
    email: str
    identification_type: IdentificationType
    identification_number: str
    phone: str | None
    hashed_password: str
    is_active: bool
