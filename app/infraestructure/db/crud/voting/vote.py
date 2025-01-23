from fastapi import HTTPException
from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.voting.vote  import Vote
from app.schemas.voting.vote import VoteCreate, VoteUpdate
from uuid import UUID

class VoteCrud(CRUDBase[Vote, VoteCreate, VoteUpdate]):
    def get_votes_by_voting(self, *, db, voting_id: UUID) -> list[Vote]:
        with db:
            response = db.query(Vote).filter(Vote.voting_id == voting_id).all()
            if not response:
                raise HTTPException(status_code=404, detail="Voting not found")
            return response

vote_crud = VoteCrud(Vote)