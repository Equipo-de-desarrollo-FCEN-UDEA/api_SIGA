# from app.infraestructure.db.utils.base import Base
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy import Column, Uuid
# import uuid
# class BaseModel(Base):
#     __abstract__ = True
#     id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
# base_model.py
from __future__ import annotations

import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID

from app.infraestructure.db.utils.base import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class BaseExposableModel(BaseModel):
    __abstract__ = True
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False)
