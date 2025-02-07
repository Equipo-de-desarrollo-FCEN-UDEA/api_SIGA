from fastapi import Depends, Security, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer, SecurityScopes
from typing import Annotated, List, Optional
from app.services.jwt import jwt_service
from jose.exceptions import JWTError
from app.core.exceptions import InvalidCredentials


from app.api.middleware.bearer import get_token

class ScopeChecker:
    def __init__(self, scopes: List[str]):
        self.parsed_scopes = self._parse_scopes(scopes)
    
    def _parse_scopes(self, scopes: List[str]) -> List[dict]:
        parsed = []
        for scope in scopes:
            parts = scope.split(':')
            if len(parts) < 2:
                continue  # Ignorar scopes mal formados
            
            where = parts[-1]
            role_parts = parts[:-1]
            parsed.append({
                "full_scope": scope,
                "role": role_parts[0],
                "type": role_parts[1] if len(role_parts) > 1 else None,
                "where": where
            })
        return parsed

    def has_scope_pattern(self, security_scopes: str) -> bool:
        print("HOLA")
        return any(scope["full_scope"] in security_scopes for scope in self.parsed_scopes)

    def has_resource_access(self, uuid: str, resource_type: Optional[str] = None) -> bool:
        return any(
            scope["uuid"] == uuid and 
            (not resource_type or scope["type"] == resource_type)
            for scope in self.parsed_scopes
        )

    def get_resources_for_type(self, resource_type: str) -> List[str]:
        return list({
            scope["uuid"] 
            for scope in self.parsed_scopes 
            if scope["type"] == resource_type
        })

def get_credentials_exception(
    security_scopes: SecurityScopes,
) -> HTTPException:
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope={security_scopes.scopes}"
    else:
        authenticate_value = "Bearer"

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

def get_current_user_scopes(
        token: Annotated[str, Depends(get_token)],
        credentials_exception: HTTPException = Depends(get_credentials_exception),
) -> ScopeChecker:
    try:
        payload = jwt_service.decode_access_token(token)
        user_id: str = payload.sub
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.scopes
    except(JWTError, InvalidCredentials):
        raise credentials_exception
    return ScopeChecker(token_scopes)

# Dependencias de seguridad personalizadas
def has_scope(
        security_scopes: SecurityScopes,
        scopes: ScopeChecker = Depends(get_current_user_scopes),
    ):

    if security_scopes.scopes and not scopes.has_scope_pattern(security_scopes.scopes):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos necesarios"
        )
    return True

