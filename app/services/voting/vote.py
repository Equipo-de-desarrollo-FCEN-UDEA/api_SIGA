from app.services.base import ServiceBase
from app.schemas.voting.vote import VoteCreate, VoteUpdate
from app.protocols.db.models.voting.vote import Vote
from app.protocols.db.crud.voting.vote import CRUDVoteProtocol
from app.errors.base import BaseErrors
from uuid import UUID

class VoteService(ServiceBase[Vote, VoteCreate, VoteUpdate, CRUDVoteProtocol]):
    def get_votes_by_voting(self, *, db, voting_id: UUID) -> list[Vote]:
        if self.observer is None:
            raise BaseErrors(code=503, detail="Service not available")
        return self.observer.get_votes_by_voting(db=db, voting_id=voting_id)

vote_svc = VoteService()