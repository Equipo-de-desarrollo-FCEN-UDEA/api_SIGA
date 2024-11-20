from uuid import UUID
from sqlalchemy.orm import Session
from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.voting.voting import Voting
from app.schemas.voting.voting import VotingCreate, VotingUpdate
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ORMError

class VotingCrud(CRUDBase[Voting, VotingCreate, VotingUpdate]):
    def get_votings_by_academic_units(self, *, db: Session,
        academic_unit_ids: list[UUID] | None = None
    ) -> list[Voting]:
        with db:
            try:
                return db.query(Voting).filter(Voting.academic_unit_id.in_(academic_unit_ids)).all()
            except IntegrityError as e:
                raise ORMError(str(e))

voting_crud = VotingCrud(Voting)