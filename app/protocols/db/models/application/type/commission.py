from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.protocols.db.utils.link_model import LinkModel
from app.protocols.db.utils.mongo_model import MongoModel


class Status(LinkModel):
    name: str
    updated_by: str
    date: datetime


class Compliment(BaseModel):
    documents: list[Any] | None = None
    emails: list[str] | None = None
    observation: str


class Commission(MongoModel):
    country: str
    state: str | None = None
    city: str | None = None
    date_start: datetime
    date_end: datetime
    reason: str
    justification: str
    status: list[Status]
    documents: list[Any] | None = None
    resolution: str | None = None
    compliment: Compliment | None = None
