from typing import Generic, TypeVar, Any
from datetime import date, datetime

from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ORMError
from app.infraestructure.db.utils.base_model import BaseModel as Model
from app.schemas.utils.base_model import UpdateSchemaType, CreateSchemaType
from app.infraestructure.db.utils.postgres_session import SessionLocal

from uuid import UUID


ModelType = TypeVar("ModelType", bound=Model)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        self.model = model

    def create(self, *, obj_in: CreateSchemaType, db: Session) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        with db:
            try:
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
                return db_obj
            except IntegrityError as e:
                raise ORMError(str(e))

    def get(self, *, id: UUID, db: Session) -> ModelType:
        with db:
            response = db.query(self.model).get(id)
            if not response:
                raise HTTPException(status_code=404, detail="Object not found")
            return response

    def get_multi(
        self,
        *,
        payload: dict[str, Any] | None = None,
        skip: int = 0,
        limit: int = 10,
        order_by: str | None = None,
        date_range: dict[str, date] | None = None,
        values: tuple[str] | None = None,
        db: Session
    ) -> list[ModelType | dict[str, Any]]:
        with db:
            try:
                return db.query(self.model).offset(skip).limit(limit).all()
            except IntegrityError as e:
                raise ORMError(str(e))

    def update(self, *, id: UUID, obj_in: UpdateSchemaType, db: Session) -> ModelType:
        obj_data = obj_in.dict()
        with db:
            try:
                db_obj = db.get(self.model, id)

                if not db_obj:
                    raise HTTPException(status_code=404, detail="Object not found")            

                mapper = inspect(self.model)

                for field in mapper.attrs:
                    if field.key in obj_data and obj_data[field.key] is not None:
                        setattr(db_obj, field.key, obj_data[field.key])
                setattr(db_obj, "updated_at", datetime.now())
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
                return db_obj
            except IntegrityError as e:
                raise ORMError(str(e))

    def delete(self, *, id: int, db: Session) -> int:
        with db:
            try:
                obj_db = db.get(self.model, id)
                db.delete(obj_db)
                db.commit()
                return True
            except IntegrityError as e:
                raise ORMError(str(e))
