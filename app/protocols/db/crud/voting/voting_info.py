from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.voting.voting_info import VotingInfo
from app.schemas.voting.voting_info import VotingInfoCreate, VotingInfoUpdate


class CRUDVotingInfoProtocol(CRUDProtocol[VotingInfo, VotingInfoCreate, VotingInfoUpdate]):
    ...