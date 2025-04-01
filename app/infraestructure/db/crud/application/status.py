from __future__ import annotations

from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.application.status import Status
from app.schemas.application.status import StatusCreate
from app.schemas.application.status import StatusUpdate


class StatusCrud(CRUDBase[Status, StatusCreate, StatusUpdate]):
    pass


status_crud = StatusCrud(Status)
