from uuid import UUID
from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.voting.voting import Voting
from app.schemas.voting.voting import VotingCreate, VotingUpdate

class CRUDVotingProtocol(CRUDProtocol[Voting, VotingCreate, VotingUpdate]):
    def get_votings_by_academic_units(self, *, db, academic_unit_ids: list[UUID]) -> list[Voting]:
        pass