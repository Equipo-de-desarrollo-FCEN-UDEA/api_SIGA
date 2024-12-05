from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.middleware.bearer import get_current_active_user
from app.api.middleware.postgres_db import get_db
from app.core.config import settings
from app.infraestructure.services.emails.user import recovery_password_email
from app.schemas.users.user import User
from app.schemas.users.user import UserCreateInDB
from app.schemas.users.user import UserUpdate
from app.services.crypt import crypt_svc
from app.services.jwt import jwt_service
from app.services.users.user import user_svc
# from app.infraestructure.db.models.user.user import User


router = APIRouter()
user_model = User


@router.post('/access-token', response_model=None)
def login_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_postgres: Annotated[Session, Depends(get_db)],
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_svc.authenticate(
        email=form_data.username,
        password=form_data.password,
        db=db_postgres,
    )
    scopes = [role.rol.scope for role in user.user_roles_academic_units]

    access_token = jwt_service.create_access_token(
        data={'sub': str(user.id), 'scopes': scopes},
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,     # Impide el acceso desde JavaScript
        # Solo en conexiones HTTPS (requiere HTTPS en producción)
        secure=settings.PRODUCTION,
        samesite=None,     # Ayuda a prevenir ataques CSRF
        path='/',
    )

    return {'message': 'Login successful'}

# Route for activate the account with the mailed token


@router.post('/activate-account/', response_model=dict)
def activate_account(
    token: str = Body(...),
    db_postgres: Session = Depends(get_db),
) -> dict:
    """ Activate account: Params:
        token: str
    """
    try:
        email = jwt_service.decode_access_token(
            token,
        ).sub
    except Exception:
        raise HTTPException(
            status_code=400, detail='Invalid token',
        )

    user: User = user_svc.get_by_email(
        email=email, db=db_postgres,
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail='El usuario con ese correo electrónico no existe',
        )

    user.is_active = True
    user_update = UserUpdate.model_validate(
        user,
    )
    user_svc.update(
        id=user.id,
        obj_in=user_update,
        db=db_postgres,
    )

    return {'msg': 'Cuenta activada correctamente'}

# Route for recovery password with email or identification


@router.post('/password-recovery/{email}', response_model=dict)
def recover_password(
    email: str, *,
    db_postgres: Session = Depends(get_db),
) -> dict:
    """
    Password Recovery
    """
    user: User = user_svc.get_by_email(
        db=db_postgres, email=email,
    ) or user_svc.get_by_identification(
        db=db_postgres, identification=email,
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail='''El usuario con este correo o número de
                      identificación no está registrado en el sistema''',
        )

    email_token = jwt_service.email_token(email=user.email)
    recovery_password_email.apply_async(
        args=(user.name, email_token, user.email),
    )
    return {
        'msg': f'''El correo para recuperar
            la contraseña fue enviado correctamente a {user.email}''',
    }

# Route for reset password


@router.post('/reset-password/', response_model=dict)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db_postgres: Session = Depends(get_db),
) -> dict:
    """
    Reset password

    Params:
        token: str
        new_password: str
    """
    try:
        email = jwt_service.decode_access_token(token).sub
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid token')

    user: UserCreateInDB = user_svc.get_by_email(
        email=email,
        db=db_postgres,
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail='''El usuario con ese
            correo electrónico no existe''',
        )

    elif not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')

    hashed_password = crypt_svc.get_password_hash(new_password)
    user.hashed_password = hashed_password
    user_update = UserUpdate.model_validate(user)
    user_svc.update(
        id=user.id,
        obj_in=user_update, db=db_postgres,
    )

    return {'msg': 'Contraseña actualizada correctamente'}


@router.get('/protected')
async def protected_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return {'message': 'Protected route'}
