from app.protocols.db.models.users.user import User
from app.protocols.db.crud.users.user import CRUDUserProtocol

from app.schemas.users.user import UserUpdate, UserCreate, UserCreateInDB, UserInDB

from app.services.base import ServiceBase
from app.services.crypt import crypt_svc

from app.infraestructure.security.jwt import jwt
from app.infraestructure.services.emails.user import confirm_email



class UserService(ServiceBase[User, UserCreateInDB, UserUpdate, CRUDUserProtocol]):
    def create(self, *, obj_in: UserCreate, db) -> User:
        hashed_password = crypt_svc.get_password_hash(obj_in.password)
        print("antes", hashed_password)
        obj = UserCreateInDB(
            **obj_in.dict(
                exclude={
                    "password",
                }
            ),
            hashed_password=hashed_password
        )
        print("depues", hashed_password)
        user = super().create(obj_in=obj, db=db)
        token = jwt.email_token(email=user.email)
        confirm_email.apply_async(args=[user.name, token, user.email])
        return user

    def authenticate(self, *, email: str, password: str, db) -> UserInDB:
        user: User = self.observer.get_by_email(email=email, db=db)
        crypt_svc.check_password(password, user.hashed_password)
        return user
    
    def get_by_email(self, *, email: str, db) -> User:
        return self.observer.get_by_email(email=email, db=db)


user_svc = UserService()
