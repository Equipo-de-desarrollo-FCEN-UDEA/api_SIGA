from __future__ import annotations

from app.protocols.db.crud.application.type.mobility import CRUDMobilityProtocol
from app.protocols.db.models.application.type.mobility import Mobility
from app.schemas.application.type.mobility import MobilityCreate
from app.schemas.application.type.mobility import MobilityUpdate
from app.services.base import ServiceBase


class MobilityService(
    ServiceBase[
        Mobility,
        MobilityCreate,
        MobilityUpdate,
        CRUDMobilityProtocol,
    ],
):
    pass


mobility_svc = MobilityService()
