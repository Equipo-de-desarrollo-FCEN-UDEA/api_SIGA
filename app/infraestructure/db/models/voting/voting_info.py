from uuid import UUID
from odmantic import Field, Model
from app.schemas.voting.voting_info import VotingStatus


class VotingInfo(Model):
    id_postgres: UUID = Field(primary_field=True)
    statuses: list[VotingStatus]