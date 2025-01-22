from datetime import date
from typing import Protocol, TypeVar, Any
from uuid import UUID

from app.schemas.utils.base_model import CreateSchemaType, UpdateSchemaType


ModelType = TypeVar("ModelType")


class CRUDProtocol(Protocol[ModelType, CreateSchemaType, UpdateSchemaType]):
    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        ...

    def get(self, *, id: UUID) -> ModelType:
        ...
        
    def get_multi(
        self,
        *,
        payload: dict[str, Any] | None = None,
        skip: int = 0,
        limit: int = 10,
        order_by: str | None = None,
        date_range: dict[str, date] | None = None,
        values: tuple[str] | None = None
    ) -> list[ModelType | dict[str, Any]]:
        ...

    def update(self, *, id: UUID, obj_in: UpdateSchemaType) -> ModelType:
        ...

    def delete(self, *, id: UUID) -> int:
        ...