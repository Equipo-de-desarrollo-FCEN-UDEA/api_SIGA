from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.link_model import LinkModel


class UserApplicationStatus(LinkModel):
    user_application_id = Column(
        Uuid, ForeignKey(
            'user_application.id',
        ), primary_key=True,
    )
    status_id = Column(Uuid, ForeignKey('status.id'), primary_key=True)
    updated_by = Column(Uuid, ForeignKey('user.id'), nullable=False)
    observation = Column(String, nullable=True)

    status = relationship('Status', back_populates='user_application_status')
    user_application = relationship(
        'UserApplication', back_populates='user_application_status',
    )
    user = relationship('User', back_populates='user_application_status')
