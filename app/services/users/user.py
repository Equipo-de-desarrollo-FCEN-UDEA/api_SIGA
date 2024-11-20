from app.protocols.db.models.users.user import User
from app.protocols.db.crud.users.user import CRUDUserProtocol

from app.schemas.users.user import UserUpdate, UserCreate, UserCreateInDB, UserInDB

from app.services.base import ServiceBase
from app.services.crypt import crypt_svc



class UserService(ServiceBase[User, UserCreateInDB, UserUpdate, CRUDUserProtocol]):
    def create(self, *, obj_in: UserCreate, db) -> User:
        hashed_password = crypt_svc.get_password_hash(obj_in.password)
        obj = UserCreateInDB(
            **obj_in.dict(
                exclude={
                    "password",
                }
            ),
            hashed_password=hashed_password
        )
        return super().create(obj_in=obj, db=db)

    def authenticate(self, *, email: str, password: str, db) -> UserInDB:
        user: User = self.observer.get_by_email(email=email, db=db)
        crypt_svc.check_password(password, user.hashed_password)
        return user
    
    def get_by_email(self, *, email: str, db) -> User:
        return self.observer.get_by_email(email=email, db=db)


user_svc = UserService()
