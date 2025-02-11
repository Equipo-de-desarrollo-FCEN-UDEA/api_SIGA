from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from fastapi.responses import JSONResponse

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.postgres_db import get_db
from app.api.middleware.scopes import has_role
from app.schemas.users.user import User
from app.schemas.voting.vote import VoteCreate
from app.services.voting.vote import vote_svc

router = APIRouter()


@router.post('', response_model=None, status_code=201)
async def create_vote(
    *,
        new_vote: VoteCreate,
        db_postgres=Depends(get_db),
        permissions: Annotated[
            str, Security(
                has_role, scopes=['votante'],
            ),
        ] = False,
        current_user: Annotated[
            User, Security(
                get_current_active_user,
            ),
        ] = None,
) -> JSONResponse:
    new_vote.user_id = current_user.id
    vote_svc.create(obj_in=new_vote, db=db_postgres)
    return JSONResponse(
        content={'message': 'vote register successfully'},
        status_code=201,
    )
