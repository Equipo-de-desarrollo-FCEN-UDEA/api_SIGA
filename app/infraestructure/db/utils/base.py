from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls):
        return cls._camel2snake(cls.__name__)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

    def _camel2snake(name: str):
        return name[0].lower() + ''.join([
            '_' + i.lower()
            if i.isupper() else i for i in name[1:]
        ]).lstrip('_')
