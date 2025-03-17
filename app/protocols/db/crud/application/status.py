from __future__ import annotations

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.application.status import Status
from app.schemas.application.status import StatusCreate
from app.schemas.application.status import StatusUpdate


class CRUDStatusProtocol(CRUDProtocol[Status, StatusCreate, StatusUpdate]):
    pass
