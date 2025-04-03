from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Identity
from sqlalchemy import Integer
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel


class UserApplication(BaseModel):
    user_id = Column(Uuid, ForeignKey('user.id'), nullable=False)
    application_id = Column(Uuid, ForeignKey('application.id'), nullable=False)
    consecutive = Column(Integer, Identity(start=5000, cycle=False), index=True)

    # relations
    user = relationship('User', back_populates='user_applications', lazy='joined')
    application = relationship(
        'Application', back_populates='user_applications', lazy='selectin',
    )
    user_application_academic_units = relationship(
        'UserApplicationAcademicUnit',
        back_populates='user_application',
        lazy='selectin',
        order_by='UserApplicationAcademicUnit.created_at.desc()',
    )
    votings = relationship('Voting', back_populates='user_application')
    user_application_users = relationship(
        'UserApplicationUser', back_populates='user_application', lazy='joined',
    )

    user_application_status = relationship(
        'UserApplicationStatus',
        back_populates='user_application',
        lazy='selectin',
        order_by='UserApplicationStatus.created_at.desc()',
    )
