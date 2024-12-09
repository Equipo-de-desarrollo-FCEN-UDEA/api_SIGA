from __future__ import annotations

from app.infraestructure.db.crud.application.type.base import (
    ApplicationTypeBaseCrud,
)
from app.infraestructure.db.models.application.type.mobility import Mobility
from app.schemas.application.type.mobility import MobilityCreate
from app.schemas.application.type.mobility import MobilityUpdate


class MobilityCrud(
    ApplicationTypeBaseCrud[Mobility, MobilityCreate, MobilityUpdate],
):
    def create(
            self,
            db_mongo,
            *,
            obj_in,
            db_postgres,
            current_user,
            application_id,
    ):
        obj_in.total_time = (obj_in.date_end - obj_in.date_start).days
        return super().create(
            db_mongo,
            obj_in=obj_in,
            db_postgres=db_postgres,
            current_user=current_user,
            application_id=application_id,
        )


mobility_crud = MobilityCrud(Mobility)
