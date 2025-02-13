from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from fastapi.responses import JSONResponse

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.mongo_db import get_mongo_db
from app.api.middleware.postgres_db import get_db
from app.api.middleware.scopes import has_role
from app.infraestructure.policies.voting.voting import (
    get_application_in_mongo,
)
from app.infraestructure.policies.voting.voting import (
    update_application_status,
)
from app.infraestructure.policies.voting.voting import voting_result
from app.schemas.users.user import User
from app.schemas.voting.vote import Vote
from app.schemas.voting.voting import VotingResponse
from app.schemas.voting.voting_info import VotingInfo
from app.schemas.voting.voting_info import VotingInfoUpdate
from app.schemas.voting.voting_info import VotingStatus
from app.services.application.user_application_academic_unit import (
    user_application_academic_unit_svc as us_app_svc,
)
from app.services.users.user_rol_academic_unit import (
    user_rol_academic_unit_svc as us_rol_svc,
)
from app.services.voting.vote import vote_svc
from app.services.voting.voting import voting_svc
from app.services.voting.voting_info import voting_info_svc

router = APIRouter()


@router.get('', response_model=list[VotingResponse], status_code=200)
def get_user_votings(
    *,
    db_postgres=Depends(get_db),
    has_permission=Security(has_role, scopes=['representante']),
    current_user: Annotated[User, Security(get_current_active_user)],
) -> list[VotingResponse]:
    VOTANTE_ROL_ID = UUID('20bd57a2-b2e2-4918-b131-8736e43f4582')
    # buscar unidades academicas donde puede votar el usuario
    academic_units = us_rol_svc.get_academic_units_by_user_id_and_rol_id(
        user_id=current_user.id, rol_id=VOTANTE_ROL_ID, db=db_postgres,
    )
    academic_unit_ids = [academic_unit.id for academic_unit in academic_units]
    votings = voting_svc.get_votings_by_academic_units(
        academic_unit_ids=academic_unit_ids, db=db_postgres,
    )
    # votings

    return votings


@router.get('/{voting_id}', response_model=dict, status_code=200)
async def get_voting(
    *,
    voting_id: UUID,
    db_postgres=Depends(get_db),
    db_mongo=Depends(get_mongo_db),
    has_permission=Security(has_role, scopes=['votante']),
) -> dict:
    voting = voting_svc.get(id=voting_id, db=db_postgres)
    voting = await get_application_in_mongo(voting=voting, db=db_mongo)
    return voting


@router.patch('/close/{voting_id}',  status_code=200)
async def close_voting(
    *,
    voting_id: UUID,
    db_postgres=Depends(get_db),
    db_mongo=Depends(get_mongo_db),
    has_permission=Security(has_role, scopes=['representante']),
    current_user: Annotated[User, Security(get_current_active_user)],
) -> JSONResponse:
    votes: list[Vote] = vote_svc.get_votes_by_voting(
        voting_id=voting_id, db=db_postgres,
    )
    result = await voting_result(votes=votes)
    new_status = VotingStatus(result=result.value, date=datetime.now())
    voting_info: VotingInfo = await voting_info_svc.get(
        id=voting_id,
        db=db_mongo,
    )
    voting_info.statuses.append(new_status)
    new_voting_info = VotingInfoUpdate(statuses=voting_info.statuses)
    await voting_info_svc.update(
        db_obj=voting_info,
        obj_in=new_voting_info,
        db=db_mongo,
    )
    voting = voting_svc.get(id=voting_id, db=db_postgres)
    await update_application_status(
        voting=voting,
        db_mongo=db_mongo,
        db_postgres=db_postgres,
        current_user=current_user,
        result=result,
    )
    us_app_svc.response(
        user_application_id=voting.user_application_id,
        academic_unit_id=voting.academic_unit_id,
        db=db_postgres,
    )

    return JSONResponse(
        status_code=200,
        content={'message': 'Votación cerrada exitosamente'},
    )
