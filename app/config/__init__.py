from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "Smart Gateway Writer"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb+srv://fyp-gch6:aBnFjBfEq8eUpMKV@gateway-database.cmu3llp.mongodb.net/test"
    DB_NAME: str = "gateway-db"


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
