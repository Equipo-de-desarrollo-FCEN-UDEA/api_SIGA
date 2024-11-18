from typing import Generic, TypeVar, Type
from uuid import UUID

from app.core.exceptions import ODMError

from odmantic import Model, ObjectId
from odmantic.session import AIOSession
from pydantic import BaseModel


ModelType = TypeVar("ModelType", bound=Model)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)



class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchema]):
    def __init__(self, model: Type[ModelType]):
        """Factory crud with odm"""
        self.model = model

    async def get(self, db: AIOSession,
                  *, id: UUID) -> ModelType:
        print(f"ID: {id}")

        return await db.find_one(self.model, self.model.id_postgres == id)
    
    async def get_multi (
                    self,
        *,
        payload: dict[str] | None = None,
        skip: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        date_range: dict[str] | None = None,
        values: tuple[str] | None = None,
        db: AIOSession
    ) -> list[ModelType]:
        return await db.find(self.model)

    async def create(self, db: AIOSession,
                     *, obj_in: Type[ModelType]) -> Type[ModelType]:
        try:
            return await db.save(obj_in)
        except Exception as e:
            raise ODMError(str(e))

    async def update(
        self,
        db: AIOSession,
        *,
        db_obj: Type[ModelType],
        obj_in: Type[UpdateSchema]
    ) -> Type[ModelType]:
        db_obj.model_update(obj_in)
        return await db.save(db_obj)

    async def delete(self, db: AIOSession, *, id: ObjectId) -> Type[ModelType]:
        db_obj = await db.find_one(self.model, self.model.id == id)
        return await db.delete(db_obj)
