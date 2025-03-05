from __future__ import annotations

from datetime import date
from typing import Any
from typing import Generic
from typing import TypeVar
from uuid import UUID

from app.errors.base import BaseErrors
from app.protocols.db.crud.base import CRUDProtocol
from app.schemas.utils.base_model import CreateSchemaType
from app.schemas.utils.base_model import UpdateSchemaType


ModelType = TypeVar('ModelType')

CrudType = TypeVar('CrudType', bound=CRUDProtocol)


class ServiceBase(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
        CrudType,
    ],
):
    def __init__(self) -> None:
        self.observer: CrudType | None = None

    def register_observer(self, observer: CrudType) -> None:
        self.observer = observer
        return None

    def unregister_observer(self) -> None:
        self.observer = None
        return None

    def create(self, *, obj_in: CreateSchemaType, db) -> ModelType:
        if self.observer is None:
            raise BaseErrors(code=503, detail='Service not available')
        return self.observer.create(obj_in=obj_in, db=db)

    def get(self, *, id: UUID, db: Any) -> ModelType:
        if self.observer is None:
            raise BaseErrors(code=503, detail='Service not available')
        return self.observer.get(id=id, db=db)

    def get_multi(
        self,
        *,
        payload: dict[str, Any] | None = None,
        skip: int = 0,
        limit: int = 10,
        order_by: str | None = None,
        date_range: dict[str, date] | None = None,
        values: tuple[str] | None = None,
        db,
    ) -> list[ModelType | dict[str, Any]]:
        if self.observer is None:
            raise BaseErrors(code=503, detail='Service not available')
        return self.observer.get_multi(
            payload=payload,
            skip=skip,
            limit=limit,
            order_by=order_by,
            date_range=date_range,
            values=values,
            db=db,
        )

    def update(
            self,
            *,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
            db,
    ) -> ModelType:
        if self.observer is None:
            raise BaseErrors(code=503, detail='Service not available')
        return self.observer.update(db_obj=db_obj, obj_in=obj_in, db=db)

    def delete(self, *, id: UUID, db) -> int:
        if self.observer is None:
            raise BaseErrors(code=503, detail='Service not available')
        return self.observer.delete(id=id, db=db)
