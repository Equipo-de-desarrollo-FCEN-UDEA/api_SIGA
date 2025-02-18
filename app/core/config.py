from __future__ import annotations

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings

from app.core.settings import DevelopAppSettings
from app.core.settings.app import AppSettings
from app.core.settings.base import AppEnv


environments: dict[AppEnv, type[AppSettings]] = {
    AppEnv.Develop: DevelopAppSettings,
    # AppEnv.Production: ProductionAppSettings,
    # AppEnv.Testing: TestingAppSettings
}


class Settings(BaseSettings):
    """
    Settings for the application.
    """

    #: The application name
    APP_NAME: str = 'auth fcen database Api'
    #: The application version
    APP_VERSION: str = '0.0.1'
    #: The application debug mode
    DEBUG: bool = False
    #: The application api version
    API_V1_STR: str = '/api/v1'

    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    # App
    APP_DOMAIN: str

    # JWT
    SECRET_KEY: str

    ALGORITHM: str = 'HS256'

    # Mongo
    mongo_url: str
    mongo_db: str

    # Redis
    redis_url: str
    redis_backend: str

    # SMTP PRODUCTION
    smtp_prod_user_email: str
    smtp_prod_user_password: SecretStr
    smtp_prod_host_email: str

    smtp_from_email: str

    # SMTP Local
    smtp_local_host_email: str
    smtp_local_port_email: int

    # URLs front
    URL_LAB: str

    # production
    PRODUCTION: bool

    # Academic units Ids
    INTERNAL_FCEN: str
    FCEN: str

    # Applications ID
    PURCHASE_ID: str


@lru_cache
def get_settings() -> BaseSettings:
    """Get the settings for the application."""
    return Settings()


settings: Settings = Settings()
