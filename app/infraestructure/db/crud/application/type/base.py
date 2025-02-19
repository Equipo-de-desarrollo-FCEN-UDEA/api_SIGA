from __future__ import annotations

from datetime import datetime
from typing import TypeVar
from uuid import UUID

from fastapi import HTTPException
from odmantic import Model
from odmantic.session import AIOSession
from pydantic import BaseModel
from pymongo.errors import PyMongoError
from sqlalchemy.orm import Session

from app.core.exceptions import ORMError
from app.infraestructure.db.crud.mongo_base import CRUDBase
from app.infraestructure.db.models.application.user_application import (
    UserApplication,
)
from app.protocols.db.models.application.application import (
    ApplicationStatusType,
)
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
            db_postgres: Session,
            current_user: User,
    ) -> ModelType:
        try:
            with db_postgres:
                db_obj = db_postgres.query(
                    UserApplication,
                ).filter_by(id=id).first()

                if not db_obj:
                    raise ORMError('User application not found')

                status = ApplicationStatusType.UPDATED.value
                obj_in.status.append(
                    UserApplicationStatus(
                        name=status,
                        updated_by=current_user.id,
                        date=datetime.now(),
                    ),
                )

                updated_obj_in = {**obj_in.dict(), 'id': db_obj.id}

                obj_updated = await super().update(
                    db_mongo,
                    db_obj=db_obj,
                    obj_in=self.model(**updated_obj_in),
                )

                db_postgres.commit()

        except Exception as e:
            db_postgres.rollback()
            raise ORMError(str(e))

        except PyMongoError as e:
            db_postgres.rollback()
            raise HTTPException(status_code=400, detail='Error: ' + str(e))

        return obj_updated

    async def add_status(
        self,
        db_mongo,
        *,
        new_status: UserApplicationStatus,
        user_application_id,
    ) -> None:
        try:
            await db_mongo.get_collection(self.model).update_one(
                {'_id': user_application_id},
                {'$push': {'status': new_status.model_dump()}},
            )

        except Exception as e:
            raise ORMError(str(e))
