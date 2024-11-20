from app.services.base import ServiceBase
from app.protocols.db.models.voting.voting_info import VotingInfo
from app.protocols.db.crud.voting.voting_info import CRUDVotingInfoProtocol
from app.schemas.voting.voting_info import VotingInfoCreate, VotingInfoUpdate

class VotingInfoService(ServiceBase[VotingInfo, VotingInfoCreate, VotingInfoUpdate, CRUDVotingInfoProtocol]):
    pass

voting_info_svc = VotingInfoService()