from __future__ import annotations

from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.infraestructure.db.crud.base import CRUDBase
from app.infraestructure.db.models.application.application import Application
from app.infraestructure.db.models.application.application_status import (
    ApplicationStatus,
)
from app.infraestructure.db.models.application.user_application import UserApplication
from app.infraestructure.services.aws.s3 import s3
from app.schemas.application.user_application import UserApplicationCreate
from app.schemas.application.user_application import UserApplicationPublic
from app.schemas.application.user_application import UserApplicationUpdate
from app.schemas.application.user_application_academic_unit import (
    UserApplicationAcademicUnitCreate,
)
from app.schemas.application.user_application_status import UserApplicationStatusCreate
from app.services.application.user_application_academic_unit import (
    user_application_academic_unit_svc,
)
from app.services.application.user_application_status import user_application_status_svc


class UserApplicationCrud(
    CRUDBase[
        UserApplication,
        UserApplicationCreate, UserApplicationUpdate,
    ],
):
    async def create_user_application(
        self,
        *,
        obj_in: UserApplicationCreate,
        user_id: UUID,
        application_id: UUID,
        academic_unit_id: UUID,
        db_postgres: Session,
        mongo_service,
        db_mongo: Session,
    ) -> UserApplicationPublic:
        user_application_create = UserApplicationCreate(
            user_id=user_id,
            application_id=application_id,
        )

        user_application = self.create(obj_in=user_application_create, db=db_postgres)

        user_application_academic_unit_create = UserApplicationAcademicUnitCreate(
            user_application_id=user_application.id,
            academic_unit_id=academic_unit_id,
        )

        user_application_academic_unit_svc.create(
            obj_in=user_application_academic_unit_create,
            db=db_postgres,
        )

        application: Application = user_application.application
        user_application_id = user_application.id
        current_user_id = user_id
        first_application_status: ApplicationStatus = application.application_status[0]
        first_application_status_id = first_application_status.status_id

        user_application_status = UserApplicationStatusCreate(
            user_application_id=user_application_id,
            status_id=first_application_status_id,
            updated_by=current_user_id,
        )
        obj_in.id = user_application.id
        created_obj = await mongo_service.create(obj_in=obj_in, db=db_mongo)

        user_application_status_svc.create(
            obj_in=user_application_status, db=db_postgres,
        )

        user_application = UserApplicationPublic.model_validate(user_application)

        user_application.info = created_obj

        return user_application

    def upload_files(
            self,
            user_application_id: UUID,
            files: list[UploadFile],
            db: Session, prefix: str | None = None,
    ) -> dict:

        user_application = user_application_crud.get(id=user_application_id, db=db)
        user_id = user_application.user_id

        dir = f'{str(user_id)}/{str(user_application_id)}/'

        for i, pdf in enumerate(files):
            if prefix:
                file_path = f'{dir}{prefix}-{i}'
            else:
                file_path = f'{dir}{pdf.filename}'
            res = s3.push_data_to_s3_bucket(
                bucket_name=settings.aws_bucket_name,
                data=pdf.file,
                file_name=file_path,
                content_type=pdf.content_type,
            )
        return res


user_application_crud = UserApplicationCrud(UserApplication)
