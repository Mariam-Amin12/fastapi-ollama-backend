from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
   
    APP_NAME: str = "FastAPI + Ollama Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_DEFAULT_MODEL: str = "llama3.2"

    OLLAMA_TIMEOUT: int = 120

    ALLOWED_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings():
    return Settings()
