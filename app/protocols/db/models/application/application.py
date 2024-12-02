from __future__ import annotations

from enum import Enum
from uuid import UUID

from app.protocols.db.utils.base_model import BaseModel


class ApplicationStatusType(Enum):
    CREATE = 'CREADA'
    IN_INSTITUTE = 'EN INSTITUTO'
    APPROVAL = 'VISTO BUENO'
    IN_COMMITEE = 'EN COMITE'
    IN_INTERNATIONAL = 'EN RELACIONES INTERNACIONALES'
    REJECTED = 'RECHAZADA'
    RETURNED = 'DEVUELTA'
    IN_DEAN = 'EN DECANATURA'
    APPROVED = 'APROBADA'


class Application(BaseModel):
    name: str
    description: str
    academic_unit_id: UUID
