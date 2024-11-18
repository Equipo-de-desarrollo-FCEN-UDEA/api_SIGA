from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi import Depends
from app.api.middleware.postgres_db import get_db
from app.schemas.users.user import User
from fastapi import Security
from app.api.middleware.bearer import get_current_active_user
from app.services.voting.vote_type import vote_type_svc

from app.schemas.voting.vote_type import VoteTypeInDB, VoteTypeCreate, VoteTypeUpdate

router = APIRouter()
@router.post("", response_model=VoteTypeInDB, status_code=201)
async def create_voting_type(*, 
    new_vote_type: VoteTypeCreate,
    db_postgres = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["admin"])
) -> VoteTypeInDB:
    vote_type = vote_type_svc.create(obj_in=new_vote_type, db=db_postgres)
    return vote_type

@router.get("", response_model=List[VoteTypeInDB])
async def get_all_voting_types(*, db_postgres = Depends(get_db)) -> List[VoteTypeInDB]:
    return vote_type_svc.get_multi(db=db_postgres)