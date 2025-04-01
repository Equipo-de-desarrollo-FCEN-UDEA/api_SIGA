from __future__ import annotations

from app.protocols.db.utils.base_model import BaseModel


class Status(BaseModel):
    name: str
    description: str
