from uuid import UUID
from app.errors.base import BaseErrors
from app.services.base import ServiceBase
from app.schemas.voting.voting import VotingCreate, VotingUpdate
from app.protocols.db.models.voting.voting import Voting
from app.protocols.db.crud.voting.voting import CRUDVotingProtocol

class VotingService(ServiceBase[Voting, VotingCreate, VotingUpdate, CRUDVotingProtocol]):
    def get_votings_by_academic_units(self, *, db, academic_unit_ids: list[UUID] | None = None) -> list[Voting]:
        if self.observer is None:
            raise BaseErrors(code=503, detail="Service not available")
        return self.observer.get_votings_by_academic_units(db=db, academic_unit_ids=academic_unit_ids)

voting_svc = VotingService()