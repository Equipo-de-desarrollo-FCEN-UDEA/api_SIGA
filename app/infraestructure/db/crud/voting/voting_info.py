from app.infraestructure.db.crud.mongo_base import CRUDBase
from app.infraestructure.db.models.voting.voting_info import VotingInfo
from app.schemas.voting.voting_info import VotingInfoCreate, VotingInfoUpdate


class VotingInfoCrud(CRUDBase[VotingInfo, VotingInfoCreate, VotingInfoUpdate]):
    pass

voting_info_crud = VotingInfoCrud(VotingInfo)