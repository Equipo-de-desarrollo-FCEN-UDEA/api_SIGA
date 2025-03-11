from __future__ import annotations

from typing import Generic
from typing import TypeVar
from uuid import UUID

from fastapi import HTTPException
from odmantic import Model
from odmantic import ObjectId
from odmantic.session import AIOSession
from pydantic import BaseModel

from app.core.exceptions import ODMError


ModelType = TypeVar('ModelType', bound=Model)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchema]):
    def __init__(self, model: type[ModelType]):
        """Factory crud with odm"""
        self.model = model

    async def get(
        self, db: AIOSession,
        *, id: UUID,
    ) -> ModelType:
        response = await db.find_one(self.model, self.model.id == id)
        if response is None:
            raise HTTPException(
                status_code=404, detail=f'{self.model.__name__} Not found',
            )
        return response

    async def get_multi(
        self,
        *,
        payload: dict[str, str] | None = None,
        skip: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        date_range: dict[str, str] | None = None,
        values: tuple[str] | None = None,
        db: AIOSession,
    ) -> list[ModelType]:
        return await db.find(self.model)

    async def create(
        self,
        db: AIOSession,
        *,
        obj_in: type[ModelType],
    ) -> type[ModelType]:
        try:
            return await db.save(obj_in)
        except Exception as e:
            raise ODMError(str(e))

    async def update(
        self,
        db: AIOSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchema,
    ) -> ModelType:
        try:
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            return await db.save(db_obj)
        except Exception as e:
            raise ODMError(f'Failed to update {self.model.__name__}: {str(e)}')

    async def delete(self, db: AIOSession, *, id: ObjectId) -> type[ModelType]:
        db_obj = await db.find_one(self.model, self.model.id == id)
        return await db.delete(db_obj)
