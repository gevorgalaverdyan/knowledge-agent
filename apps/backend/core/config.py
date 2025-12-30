from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEMINI_GENAI_MODEL: str
    GEMINI_API_KEY: str
    GEMINI_EMBEDDING_MODEL: str
    DB_URL: str
    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    return Settings() # type: ignore
