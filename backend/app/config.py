from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "ElectroPMS"
    APP_ENV: str = "development"
    DATABASE_URL: str = "postgresql://electropms:secret@localhost:5432/electropms"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080
    ANTHROPIC_API_KEY: str = ""
    LINE_CHANNEL_ID: str = ""
    LINE_CHANNEL_SECRET: str = ""
    LINE_CHANNEL_ACCESS_TOKEN: str = ""
    LINE_LOGIN_CALLBACK_URL: str = "http://localhost:8000/api/auth/line/callback"
    FACEBOOK_APP_ID: str = ""
    FACEBOOK_APP_SECRET: str = ""
    FACEBOOK_CALLBACK_URL: str = "http://localhost:8000/api/auth/facebook/callback"
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_CALLBACK_URL: str = "http://localhost:8000/api/auth/google/callback"
    CORS_ORIGINS: str = "http://localhost:5173,capacitor://localhost"
    UPLOAD_DIR: str = "./uploads"
    UPLOAD_MAX_SIZE_MB: int = 50

    class Config:
        env_file = ".env"
        extra = "allow"

@lru_cache()
def get_settings():
    return Settings()
