from datetime import timedelta, datetime, timezone

from jose import jwt as jose_jwt
from jose.exceptions import JWTError

from app.core.config import settings
from app.core.exceptions import InvalidCredentials
from app.schemas.token import TokenPayload


class JWT:
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expires = datetime.now(timezone.utc) + expires_delta
        else:
            expires = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expires})
        token = jose_jwt.encode(
            to_encode,
            str(settings.SECRET_KEY),
            algorithm=settings.ALGORITHM,
        )
        return token
    
    def email_token(self, email: str) -> str:
        data = {"sub": email}
        return self.create_access_token(data, expires_delta=timedelta(hours=24))

    def decode_access_token(self, token: str) -> TokenPayload:
        try:
            payload = jose_jwt.decode(
                token, str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM]
            )
            return TokenPayload(**payload)
        except JWTError:
            raise InvalidCredentials("Invalid access token")


jwt = JWT()
