from __future__ import annotations

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.link_model import LinkModel


class UserApplicationAcademicUnit(LinkModel):
    user_application_id = Column(
        Uuid, ForeignKey(
            'user_application.id',
        ), nullable=False, primary_key=True,
    )
    academic_unit_id = Column(
        Uuid, ForeignKey(
            'academic_unit.id',
        ), nullable=False, primary_key=True,
    )
    is_active = Column(Boolean, nullable=False, default=True)

    # relations
    user_application = relationship(
        'UserApplication',
        back_populates='user_application_academic_units', lazy='joined',
    )
    academic_unit = relationship(
        'AcademicUnit',
        back_populates='user_application_academic_units', lazy='joined',
    )

    class config:
        orm_mode = True
