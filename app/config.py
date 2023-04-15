from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_uri: str
    api_key: str

    # Read from .env file
    class Config:
        env_file = "app/.env"

# cache contents of env file
@lru_cache()
def get_settings():
    return Settings()