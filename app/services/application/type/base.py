from __future__ import annotations

from typing import Annotated
from typing import TypeVar
from uuid import UUID

from odmantic.session import AIOSession
from sqlalchemy.orm import Session

from app.errors.base import BaseErrors
from app.infraestructure.services.emails.application import update_status_email
from app.protocols.db.crud.base import CRUDProtocol
from app.schemas.application.user_application import UserApplicationStatus
from app.schemas.utils.base_model import CreateSchemaType
from app.schemas.utils.base_model import UpdateSchemaType
from app.services.application.user_application import user_application_svc
from app.services.base import ServiceBase

ModelType = TypeVar('ModelType')

CrudType = TypeVar('CrudType', bound=CRUDProtocol)


class ApplicationTypeBaseService(
    ServiceBase[ModelType, CreateSchemaType, UpdateSchemaType, CrudType],
):

    def create(
        self, *,
        obj_in: CreateSchemaType,
        db_mongo: AIOSession,
        db_postgres: Session,
        current_user: Annotated,
        application_id: str,
    ) -> CreateSchemaType:

        if self.observer is None:
            raise BaseErrors(code=503, detail='Service not available')

        return self.observer.create(
            obj_in=obj_in,
            db_mongo=db_mongo,
            db_postgres=db_postgres,
            current_user=current_user,
            application_id=application_id,
        )

    async def update(
        self, *,
        id: UUID,
        obj_in: UpdateSchemaType,
        db_mongo: AIOSession,
    ) -> UpdateSchemaType:

        if self.observer is None:
            raise BaseErrors(code=503, detail='Service not available')

        return await self.observer.update(
            id=id,
            obj_in=obj_in,
            db_mongo=db_mongo,
        )

    async def add_status(
        self, *,
        new_status: UserApplicationStatus,
        db_mongo: AIOSession,
        db_postgres: Session,
        user_application_id: UUID,
    ):
        if self.observer is None:
            raise BaseErrors(code=503, detail='Service not available')

        user_application = user_application_svc.get(
            id=user_application_id,
            db=db_postgres,
        )

        document = await self.observer.add_status(
            new_status=new_status,
            db_mongo=db_mongo,
            user_application_id=user_application_id,
        )

        status = document['status'][-1]

        update_status_email.apply_async(
            args=[
                user_application.application.name,
                status['name'],
                status['name'],
                user_application_id,
                user_application.user.email,
            ],
        )

        return document
