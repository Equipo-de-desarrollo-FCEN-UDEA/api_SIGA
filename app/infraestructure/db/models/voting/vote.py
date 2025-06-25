from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.link_model import LinkModel


class Vote(LinkModel):

    voting_id = Column(
        Integer, ForeignKey('voting.id'),
        nullable=False, primary_key=True,
    )
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
    vote_type_id = Column(Integer, ForeignKey('vote_type.id'), nullable=False)

    # relations
    voting = relationship('Voting', back_populates='votes')
    user = relationship('User', back_populates='votes')
    vote_type = relationship('VoteType', back_populates='votes', lazy='joined')
