from datetime import datetime
from typing import TypeVar
from fastapi import HTTPException
from odmantic import AIOEngine, Model
from pydantic import BaseModel
from app.core.exceptions import ORMError
from pymongo.errors import PyMongoError
from app.infraestructure.db.crud.mongo_base import CRUDBase
from app.schemas.application.user_application import UserApplicationStatus

from app.infraestructure.db.models.application.user_application import UserApplication
from app.schemas.application.user_application import UserApplicationCreate
from app.protocols.db.models.application.application import ApplicationStatusType

from app.schemas.users.user import User

from odmantic.session import AIOSession
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Model)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

class ApplicationTypeBaseCrud(CRUDBase[ModelType, CreateSchemaType, UpdateSchema]):
    async def create(self, db_mongo: AIOSession,
                     *, obj_in: CreateSchemaType,
                     db_postgres: Session,
                     current_user: User,
                     application_id: str
                     ) -> ModelType:
        user_application = UserApplicationCreate(user_id=current_user.id, application_id=application_id)
        obj_in_data = user_application.model_dump()
        db_obj = UserApplication(**obj_in_data)
        try:
            with db_postgres:
                db_postgres.add(db_obj)
                db_postgres.flush()
                
                obj_in.id_postgres = db_obj.id

                status = ApplicationStatusType.CREATE.value
                obj_in.status += [UserApplicationStatus(name=status, updated_by=current_user.id, date=datetime.now())]
                
                obj_create = await super().create(db_mongo, obj_in=self.model(**dict(obj_in)))
                db_postgres.commit()

        except Exception as e:
            db_postgres.rollback()
            raise ORMError(str(e))
        
        except PyMongoError as e:
            db_postgres.rollback()
            raise HTTPException(status_code=400, detail= "Error: " + str(e))

        
        return obj_create
    
    async def add_status(self, db_mongo, *, new_status: UserApplicationStatus, user_application_id) -> None:
        try: 
            await db_mongo.get_collection(self.model).update_one(
                {"_id": user_application_id},
                {"$push": {"status": new_status.model_dump()}}
            )

        except Exception as e:
            raise ORMError(str(e))
