from datetime import datetime
from enum import Enum
from app.protocols.db.utils.mongo_model import MongoModel

class VotingResult(Enum):
    APPROVED = "APROBADO"
    REJECTED = "RECHAZADO"
    PENDING = "PENDIENTE"
    MEETING = "REUNION"

class VotingStatus():
    result: VotingResult
    date: datetime
    observation: str | None

class VotingInfo(MongoModel):
    statuses: list[VotingStatus]

