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
    LLM_MODEL_NAME: str = "qwen3:1.7b"
    LLM_BASE_URL: str = "http://192.168.1.36:11434/"

settings = Settings()
