from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import SecurityScopes
from jose.exceptions import JWTError

from app.api.middleware.bearer import get_credentials_exception
from app.api.middleware.bearer import get_token
from app.core.exceptions import InvalidCredentials
from app.services.jwt import jwt_service

NO_PERMISSIONS = 'No tienes los permisos necesarios'


class ScopeChecker:
    def __init__(self, scopes: list[str]):
        self.parsed_scopes = self._parse_scopes(scopes)

    def _parse_scopes(self, scopes: list[str]) -> list[dict]:
        parsed = []
        for scope in scopes:
            parts = scope.split(':')
            if len(parts) < 2:
                continue  # Ignorar scopes mal formados

            where = parts[-1]
            role_parts = parts[:-1]
            parsed.append({
                'full_scope': scope,
                'role': role_parts[0],
                'type': role_parts[1] if len(role_parts) > 1 else None,
                'where': where,
            })
        return parsed

    def has_scope_pattern(self, security_scopes: str) -> bool:
        return any(
            scope['full_scope'] in security_scopes
            for scope in self.parsed_scopes
        )

    def has_role(self, security_roles: list[str]) -> bool:
        return any(
            scope['role'] in security_roles for scope in self.parsed_scopes
        )


def get_current_user_scopes(
        token: Annotated[str, Depends(get_token)],
        credentials_exception: HTTPException = Depends(
            get_credentials_exception,
        ),
) -> ScopeChecker:
    try:
        payload = jwt_service.decode_access_token(token)
        user_id: str = payload.sub
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.scopes
    except (JWTError, InvalidCredentials):
        raise credentials_exception
    return ScopeChecker(token_scopes)

# Dependencias de seguridad personalizadas


def has_scope(
        security_scopes: SecurityScopes,
        scopes: ScopeChecker = Depends(get_current_user_scopes),
):

    if security_scopes.scopes and not scopes.has_scope_pattern(
        security_scopes.scopes,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=NO_PERMISSIONS,
        )
    return True


def has_role_in_academic_unit(role: str):
    def dependency(
            academic_unit_id: UUID,
            scopes: ScopeChecker = Security(get_current_user_scopes),
    ):
        required_scope = f'{role}:{academic_unit_id}'
        if not scopes.has_scope_pattern(required_scope):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=NO_PERMISSIONS,
            )
        return True
    return dependency  # Retorna la función sin ejecutarla


def has_role(
        security_roles: SecurityScopes,
        scopes: ScopeChecker = Depends(get_current_user_scopes),
):

    if security_roles.scopes and not scopes.has_role(security_roles.scopes):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=NO_PERMISSIONS,
        )
    return True
