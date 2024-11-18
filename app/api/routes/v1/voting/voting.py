from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Security
from app.api.middleware.bearer import get_current_active_user
from app.schemas.users.user import User
from app.schemas.voting.voting import VotingInDB, VotingResponse
from app.infraestructure.db.models.voting.voting import Voting
from app.api.middleware.postgres_db import get_db
from app.api.middleware.mongo_db import get_mongo_db
from app.services.voting.voting import voting_svc
from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc

from app.infraestructure.policies.voting.voting import get_application_in_mongo

router = APIRouter()

@router.get("", response_model=list[VotingResponse], status_code=200)
def get_user_votings(
    *,
    db_postgres = Depends(get_db),
    current_user: Annotated[User, Security(get_current_active_user, scopes=["votante"])]
) -> list[VotingResponse]:
    VOTANTE_ROL_ID = UUID('20bd57a2-b2e2-4918-b131-8736e43f4582')
    #buscar unidades academicas donde puede votar el usuario
    academic_units = user_rol_academic_unit_svc.get_academic_units_by_user_id_and_rol_id(user_id=current_user.id, rol_id=VOTANTE_ROL_ID, db=db_postgres)
    academic_unit_ids = [academic_unit.id for academic_unit in academic_units]
    votings = voting_svc.get_votings_by_academic_units(academic_unit_ids=academic_unit_ids, db=db_postgres)
    #votings

    return votings

@router.get("/{voting_id}", response_model=dict, status_code=200)
async def get_voting(*,
    voting_id: UUID,
    db_postgres = Depends(get_db),
    db_mongo = Depends(get_mongo_db),
    current_user: Annotated[User, Security(get_current_active_user, scopes=["votante"])]
) -> dict:
    voting = voting_svc.get(id=voting_id, db=db_postgres)
    voting = await get_application_in_mongo(voting=voting, db=db_mongo)
    return voting
