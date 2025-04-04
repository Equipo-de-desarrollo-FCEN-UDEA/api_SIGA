from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import SecurityScopes
from jose.exceptions import JWTError

from app.api.middleware.postgres_db import get_db
from app.core.config import settings
from app.core.exceptions import InvalidCredentials
from app.protocols.db.models.users.user import User
from app.schemas.token import TokenPayload
from app.services.jwt import jwt_service
from app.services.users.user import user_svc

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f'http://localhost:8003{settings.API_V1_STR}/auth/access-token',
)


def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No Authenticated',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return token


def get_credentials_exception(
    security_scopes: SecurityScopes,
) -> HTTPException:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope={security_scopes.scopes}'
    else:
        authenticate_value = 'Bearer'

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value},
    )


def get_current_user_db(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(get_token)],
        credentials_exception: HTTPException = Depends(get_credentials_exception),
        db=Depends(get_db),
) -> User:

    try:
        payload = jwt_service.decode_access_token(token)
        username: str = payload.sub
        if username is None:
            raise credentials_exception
        token_scopes = payload.scopes
        token_data = TokenPayload(scopes=token_scopes, sub=username)
    except (JWTError, InvalidCredentials):
        raise credentials_exception

    user = user_svc.get(id=token_data.sub, db=db)
    if user is None:
        raise credentials_exception

    if security_scopes.scopes and not any(
        scope in token_data.scopes for scope in security_scopes.scopes
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not enough permissions',
        )

    return user


def get_current_user(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(get_token)],
        credentials_exception: HTTPException = Depends(get_credentials_exception),
) -> User:

    try:
        payload = jwt_service.decode_access_token(token)
        user_id: str = payload.sub
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.scopes
        token_data = TokenPayload(scopes=token_scopes, sub=user_id, info=payload.info)
    except (JWTError, InvalidCredentials):
        raise credentials_exception

    user = token_data.info
    if user is None:
        raise credentials_exception

    if security_scopes.scopes and not any(
        scope in token_data.scopes for scope in security_scopes.scopes
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not enough permissions',
        )
    user = {**user, 'id': user_id, 'scopes': token_data.scopes}

    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user_db)],
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
