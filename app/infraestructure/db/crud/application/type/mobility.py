from __future__ import annotations

from app.infraestructure.db.crud.mongo_base import CRUDBase
from app.infraestructure.db.models.application.type.mobility import Mobility
from app.schemas.application.type.mobility import MobilityCreate
from app.schemas.application.type.mobility import MobilityUpdate


class MobilityCrud(
    CRUDBase[Mobility, MobilityCreate, MobilityUpdate],
):
    pass


mobility_crud = MobilityCrud(Mobility)
