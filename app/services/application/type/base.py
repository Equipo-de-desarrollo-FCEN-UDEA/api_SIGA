from typing import TypeVar
from app.errors.base import BaseErrors
from app.services.base import ServiceBase
from app.schemas.utils.base_model import CreateSchemaType, UpdateSchemaType

from typing import Annotated
from odmantic.session import AIOSession
from uuid import UUID
from sqlalchemy.orm import Session

from app.protocols.db.crud.application.user_application import CRUDUserApplicationProtocol
from app.schemas.application.user_application import UserApplicationStatus

ModelType = TypeVar("ModelType")

CrudType = TypeVar("CrudType", bound=CRUDUserApplicationProtocol)

class ApplicationTypeBaseService(ServiceBase[ModelType, CreateSchemaType, UpdateSchemaType, CrudType]):
    def create(self, *, 
                obj_in: CreateSchemaType, 
                db_mongo: AIOSession,
                db_postgres: Session,
                current_user: Annotated,
                application_id: str
               ) -> CreateSchemaType:
        if self.observer is None:
            raise BaseErrors(code=503, detail="Service not available")
        return self.observer.create(obj_in=obj_in, db_mongo=db_mongo, db_postgres=db_postgres, current_user=current_user, application_id=application_id)
    
    def update(self, *, 
               id: UUID, 
               obj_in: UpdateSchemaType,
               db_mongo: AIOSession, 
               db_postgres: Session, 
               current_user: Annotated
              ) -> UpdateSchemaType:
        if self.observer is None:
            raise BaseErrors(code=503, detail="Service not available")
        return self.observer.update(id=id, obj_in=obj_in, db_mongo=db_mongo, db_postgres=db_postgres, current_user=current_user)
    
    def add_status(self, *, 
                   new_status: UserApplicationStatus, 
                   db_mongo: AIOSession, 
                   user_application_id: UUID):
        if self.observer is None:
            raise BaseErrors(code=503, detail="Service not available")
        return self.observer.add_status(new_status=new_status, db_mongo=db_mongo, user_application_id=user_application_id)
