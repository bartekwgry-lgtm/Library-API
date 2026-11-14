"""Application settings loaded from the environment."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration.

    :ivar app_name: OpenAPI title
    :ivar debug: enable SQLAlchemy SQL echo when ``True``
    :ivar database_url: async SQLAlchemy database URL
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Library API"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://library:library@localhost:5432/library"


settings = Settings()
