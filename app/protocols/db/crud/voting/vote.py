from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.voting.vote import Vote
from app.schemas.voting.vote import VoteCreate, VoteUpdate
from sqlalchemy.orm import Session
from uuid import UUID

class CRUDVoteProtocol(CRUDProtocol[Vote, VoteCreate, VoteUpdate]):
    def get_votes_by_voting(self, *, db: Session, voting_id: UUID) -> list[Vote]:
        pass