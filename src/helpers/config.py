from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    GIT_TOKEN: str
    FILE_ALLOWED_EXTENSIONS: list
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int
    MONGODB_URL: str
    MONGODB_DB: str

    GENERATION_BACKEND:str
    EMBEDDING_BACKEND:str

    OPENAI_API_KEY:str = None
    OPENAI_API_URL:str = None
    COHERE_API_KEY:str = None

    GENERATION_MODLE_ID:str = None
    EMBEDDING_MODLE_ID:str = None
    EMBEDDING_MODLE_SIZE:int = None

    INPUT_DEFAULT_MAX_CARACTERS:int = None    
    GENERATION_DEFAULT_MAX_TOKENS:int = None
    GENERATION_DEFAULT_TEMPRATURE:float = None
    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
