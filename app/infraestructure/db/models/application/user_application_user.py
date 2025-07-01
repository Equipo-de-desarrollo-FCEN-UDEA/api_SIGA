from __future__ import annotations

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.link_model import LinkModel


class UserApplicationUser(LinkModel):
    user_application_id = Column(
        Integer, ForeignKey(
            'user_application.id',
        ), nullable=False, primary_key=True,
    )
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
    is_active = Column(Boolean, nullable=False, default=True)

    # relations
    user_application = relationship(
        'UserApplication', back_populates='user_application_users', lazy='joined',
    )
    user = relationship('User', back_populates='user_applications_user', lazy='joined')

    class config:
        orm_mode = True
