from __future__ import annotations

from datetime import datetime
from typing import TypeVar
from uuid import UUID

from odmantic import Model
from odmantic.session import AIOSession
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.exceptions import ORMError
from app.infraestructure.db.crud.mongo_base import CRUDBase
from app.schemas.application.user_application import UserApplicationCreate
from app.schemas.application.user_application import UserApplicationStatus
from app.schemas.users.user import User
from app.services.application.user_application import user_application_svc

ModelType = TypeVar('ModelType', bound=Model)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class ApplicationTypeBaseCrud(
    CRUDBase[ModelType, CreateSchemaType, UpdateSchema],
):
    async def create(
        self, db_mongo: AIOSession,
        *, obj_in: CreateSchemaType,
        db_postgres: Session,
        current_user: User,
        application_id: str,
    ) -> ModelType:
        user_application_create = UserApplicationCreate(
            user_id=current_user.id, application_id=application_id,
        )
        user_application = user_application_svc.create(
            obj_in=user_application_create, db=db_postgres,
        )

        obj_in.id = user_application.id

        create_status = UserApplicationStatus(
            name='CREADA',
            updated_by=current_user.id,
            date=datetime.now(),
        )
        obj_in.status = [create_status]

        obj_create = await super().create(
            db_mongo,
            obj_in=self.model(**dict(obj_in)),
        )

        return obj_create

    async def update(
            self,
            db_mongo: AIOSession,
            *,
            id: UUID,
            obj_in: UpdateSchema,
    ) -> ModelType:
        db_obj = await super().get(db_mongo, id=id)
        obj_updated = await super().update(
            db_mongo,
            db_obj=db_obj,
            obj_in=obj_in,
        )

        return obj_updated

    async def add_status(
        self,
        db_mongo,
        *,
        new_status: UserApplicationStatus,
        user_application_id,
    ):
        try:
            res = await db_mongo.get_collection(self.model).update_one(
                {'_id': user_application_id},
                {'$push': {'status': new_status.model_dump()}},
            )
            if res.modified_count == 1:
                updated_document = await db_mongo.get_collection(
                    self.model,
                ).find_one(
                    {'_id': user_application_id},
                )
                return updated_document
            else:
                raise ORMError('Failed to update the document')

        except Exception as e:
            raise ORMError(str(e))
