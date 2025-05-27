from __future__ import annotations

from fastapi import HTTPException

from app.infraestructure.security.jwt import jwt
from app.infraestructure.services.emails.user import confirm_email
from app.protocols.db.crud.users.user import CRUDUserProtocol
from app.protocols.db.models.users.user import User
from app.infraestructure.db.models.user.user import User as UserORM
from app.schemas.users.user import UserCreate
from app.schemas.users.user import UserCreateInDB
from app.schemas.users.user import UserInDB
from app.schemas.users.user import UserUpdate
from app.services.base import ServiceBase
from app.services.crypt import crypt_svc
from sqlalchemy import select, func
from typing import Optional
from sqlalchemy.orm import Session



class UserService(
    ServiceBase[
        User,
        UserCreateInDB,
        UserUpdate,
        CRUDUserProtocol,
    ],
):
    def create(self, *, obj_in: UserCreate, db) -> User:
        hashed_password = crypt_svc.get_password_hash(obj_in.password)
        obj = UserCreateInDB(
            **obj_in.dict(
                exclude={
                    'password',
                },
            ),
            hashed_password=hashed_password,
        )
        user = super().create(obj_in=obj, db=db)
        token = jwt.email_token(email=user.email)
        confirm_email.apply_async(args=[user.name, token, user.email])
        return user

    def authenticate(self, *, email: str, password: str, db) -> UserInDB:
        user: User = self.observer.get_by_email(email=email, db=db)
        if not user.is_active:
            raise HTTPException(status_code=400, detail='Inactive user')
        crypt_svc.check_password(password, user.hashed_password)
        return user

    def get_by_email(self, *, email: str, db) -> User:
        return self.observer.get_by_email(email=email, db=db)

    def get_by_identification(
            self, *, identification_number: str, db,
    ) -> User:
        return self.observer.get_by_identification(
            identification_number=identification_number,
            db=db,
        )
    def count(self, db):
        stmt = select(func.count()).select_from(UserORM)
        result = db.execute(stmt)
        return result.scalar_one()
    
    
    def get_filtered_users(self, skip: int, limit: int, name: Optional[str], email: Optional[str], identification_number: Optional[str], db: Session):
        query = db.query(UserORM)

        if name:
            query = query.filter(UserORM.name.ilike(f"%{name.strip()}%"))
        if email:
            query = query.filter(UserORM.email.ilike(f"%{email.strip()}%"))
        if identification_number:
            query = query.filter(UserORM.identification_number.ilike(f"%{identification_number.strip()}%"))

        total = query.count()
        users = query.offset(skip).limit(limit).all()

        return total, users



user_svc = UserService()
