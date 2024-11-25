from __future__ import annotations

from uuid import UUID

from odmantic import Field
from odmantic import Model

from app.schemas.voting.voting_info import VotingStatus


class VotingInfo(Model):
    id: UUID = Field(primary_field=True)
    statuses: list[VotingStatus]
