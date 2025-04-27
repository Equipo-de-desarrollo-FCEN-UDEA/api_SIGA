from __future__ import annotations

from app.protocols.db.crud.base import CRUDProtocol
from app.protocols.db.models.users.user import User
from app.schemas.users.user import UserCreateInDB
from app.schemas.users.user import UserUpdate


class CRUDUserProtocol(CRUDProtocol[User, UserCreateInDB, UserUpdate]):

    def get_by_email(self, *, email: str) -> User:
        ...

    def get_by_identification(self, *, identification_number: str) -> User:
        ...

    def get_multi(self, *, skip: int = 0, limit: int = 10) -> list[User]:
        ...
