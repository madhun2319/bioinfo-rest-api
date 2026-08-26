from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    NCBI_API_KEY: str | None = None
    APP_API_KEY: str | None = None
    REDIS_URL: str = "redis://localhost:6379"
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = {"env_file": ".env"}


settings = Settings()
