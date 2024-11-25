from __future__ import annotations

from datetime import datetime
from typing import Any

from app.protocols.db.utils.link_model import LinkModel
from app.protocols.db.utils.mongo_model import MongoModel


class Status(LinkModel):
    name: str
    updated_by: str
    date: datetime


class Commission(MongoModel):
    country: str
    state: str | None
    city: str | None
    date_start: datetime
    date_end: datetime
    reason: str
    justification: str
    status: list[Status]
    documents: list[Any] | None
    resolution: str | None
    compliment: Any | None
