from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.link_model import LinkModel


class ApplicationStatus(LinkModel):
    application_id = Column(Uuid, ForeignKey('application.id'), primary_key=True)
    status_id = Column(Uuid, ForeignKey('status.id'), primary_key=True)
    step = Column(Integer, nullable=False)

    application = relationship('Application', back_populates='application_status')
    status = relationship('Status', back_populates='application_status', lazy='joined')
