from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings (BaseSettings):
    APP_NAME : str
    APP_VERSION : str
    GIT_TOKEN:str
    FILE_ALLOWED_EXTENSIONS : list
    FILE_MAX_SIZE : int
    FILE_CHUNK_SIZE : int
    MONGODB_URL : str
    MONGODB_DB : str
    class Config:
        env_file=".env"
def get_settings ():
    return Settings()