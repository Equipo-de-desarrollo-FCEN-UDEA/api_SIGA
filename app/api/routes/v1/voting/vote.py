from fastapi import APIRouter
from fastapi import Depends, Security
from fastapi.responses import JSONResponse
from typing import Annotated
from app.schemas.users.user import User
from app.api.middleware.bearer import get_current_active_user


from app.api.middleware.postgres_db import get_db
from app.schemas.voting.vote import VoteCreate
from app.services.voting.vote import vote_svc

router = APIRouter()

@router.post("", response_model=None, status_code=201)
async def create_vote(*, 
        new_vote: VoteCreate, 
        db_postgres = Depends(get_db),
        current_user: Annotated[User, Security(get_current_active_user, scopes=["votante"])] = None
    ) -> JSONResponse:
    new_vote.user_id = current_user.id
    vote_svc.create(obj_in=new_vote, db=db_postgres)
    return JSONResponse(content={"message": "vote register successfully"}, status_code=201)