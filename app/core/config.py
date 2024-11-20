from functools import lru_cache
from locale import setlocale, LC_TIME
from typing import Any, Dict, List, Type

from app.core.settings.app import AppSettings
from app.core.settings.base import AppEnv, BaseAppSettings
from app.core.settings import DevelopAppSettings

from pydantic_settings import BaseSettings


environments: Dict[AppEnv, Type[AppSettings]] = {
    AppEnv.Develop: DevelopAppSettings
    # AppEnv.Production: ProductionAppSettings,
    # AppEnv.Testing: TestingAppSettings
}



class Settings(BaseSettings):
    """
    Settings for the application.
    """

    #: The application name
    APP_NAME: str = "auth fcen database Api"
    #: The application version
    APP_VERSION: str = "0.0.1"
    #: The application debug mode
    DEBUG: bool = False
    #: The application api version
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    SECRET_KEY: str 

    ALGORITHM: str = "HS256"

    ## Mongo
    mongo_url:str
    mongo_db:str

    #: Postgres database url
    database_url:str

    ## Redis
    redis_url:str
    redis_backend:str



@lru_cache()
def get_settings() -> BaseSettings:
    """Get the settings for the application."""
    return Settings()


settings: Settings = Settings()
