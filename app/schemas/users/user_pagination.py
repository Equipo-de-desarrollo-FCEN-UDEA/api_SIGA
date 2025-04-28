# app/schemas/users/user_pagination.py
from pydantic import BaseModel
from typing import List
from app.schemas.users.user import UserInDB

class PaginatedUsers(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    users: List[UserInDB]