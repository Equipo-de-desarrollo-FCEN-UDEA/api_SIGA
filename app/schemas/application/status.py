from __future__ import annotations

from pydantic import BaseModel


class StatusBase(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class StatusCreate(StatusBase):
    pass


class StatusUpdate(BaseModel):
    name: str | None
    description: str | None


class StatusPublic(StatusBase):
    pass
