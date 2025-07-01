from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseExposableModel


class Voting(BaseExposableModel):
    academic_unit_id = Column(Integer, ForeignKey('academic_unit.id'), nullable=False)
    user_application_id = Column(
        Integer, ForeignKey(
            'user_application.id',
        ), nullable=False,
    )

    # relations
    academic_unit = relationship('AcademicUnit', back_populates='votings', lazy='joined')
    user_application = relationship(
        'UserApplication', back_populates='votings', lazy='joined',
    )
    votes = relationship('Vote', back_populates='voting', lazy='joined')
