from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.api.middleware.bearer import get_current_active_user
from app.schemas.users.user import User
from app.services.users.user import user_svc
from app.services.jwt import jwt_service
from app.schemas.token import Token
from app.core.config import settings

from app.api.middleware.postgres_db import get_db


router = APIRouter()


@router.post("/access-token", response_model=None)
def login_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_postgres: Annotated[Session, Depends(get_db)]):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_svc.authenticate(
        email=form_data.username,
        password=form_data.password,
        db=db_postgres
    )
    scopes = [role.rol.scope for role in user.user_roles_academic_units]

    access_token = jwt_service.create_access_token(
        data = {"sub": str(user.id), "scopes": scopes}, expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,     # Impide el acceso desde JavaScript
        secure=True,       # Solo en conexiones HTTPS (requiere HTTPS en producción)
        samesite="Lax",     # Ayuda a prevenir ataques CSRF
        path="/",
    )

    return {"message": "Login successful"}

@router.get("/protected")
async def protected_route(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {"message": "Protected route"}

