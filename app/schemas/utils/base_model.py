from __future__ import annotations

from datetime import datetime
from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel


CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel, contravariant=True)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel, contravariant=True)
ObjInDB = TypeVar('ObjInDB', bound=BaseModel)


class GeneralResponse(BaseModel):
    id: UUID
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes = True
