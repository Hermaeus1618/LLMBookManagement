import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #
    # General
    #
    DEBUG: bool = True
    SECRET_KEY: str = "strongpassword"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    #
    # Database
    #
    POSTGRES_USER: str = "pyuser"
    POSTGRES_PASSWORD: str = "12345678"
    POSTGRES_DB: str = "books"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    #
    # LLM / AI
    #
    LLM_PROVIDER: str = "openrouter"
    LLM_MODEL_NAME: str = "llama-3-8b"
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL: str = "https://api.openrouter.ai"


settings = Settings()
