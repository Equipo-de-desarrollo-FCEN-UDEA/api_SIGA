from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


@as_declarative()
class Base(DeclarativeBase):
    __name__: str

    @declared_attr
    def __tablename__(cls):
        return cls._camel2snake(cls.__name__)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

    @staticmethod
    def _camel2snake(name: str):
        return name[0].lower() + ''.join([
            '_' + i.lower()
            if i.isupper() else i for i in name[1:]
        ]).lstrip('_')
