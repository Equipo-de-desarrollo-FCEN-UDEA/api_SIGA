from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel


class Status(BaseModel):
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    user_application_status = relationship(
        'UserApplicationStatus', back_populates='status',
    )
