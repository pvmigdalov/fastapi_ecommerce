from typing import Annotated

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    database_url: Annotated[str, Field(..., alias="DATABASE_URL")]

    model_config = SettingsConfigDict(
        env_file="app/settings/db.env",
        env_file_encoding="utf-8",
    )


class AuthSettings(BaseSettings):
    jwt_algorithm: Annotated[str, Field(default="HS256", alias="JWT_ALGORITHM")]
    jwt_secret_key: Annotated[SecretStr, Field(..., alias="JWT_SECRET_KEY")]

    model_config = SettingsConfigDict(
        env_file="app/settings/auth.env",
        env_file_encoding="utf-8",
    )


class Settings(BaseSettings):
    db_settings: Annotated[DBSettings, Field(default_factory=DBSettings)]
    auth_settings: Annotated[AuthSettings, Field(default_factory=AuthSettings)]


settings = Settings()
