from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel


class Status(BaseModel):
    name = Column(str, nullable=False)
    description = Column(str, nullable=True)
