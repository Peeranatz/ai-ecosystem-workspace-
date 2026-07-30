import os
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Ecosystem API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security / JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # PostgreSQL Configuration
    POSTGRES_HOST: str = os.getenv("POSTGRE_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRE_PORT", "5433")
    POSTGRES_USER: str = os.getenv("POSTGRE_USER", "labelstudio_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRE_PASSWORD", "labelstudio_password")
    POSTGRES_DB: str = os.getenv("POSTGRE_NAME", "labelstudio")
    
    # MinIO Configuration
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ROOT_USER: str = os.getenv("MINIO_ROOT_USER", "minioadmin")
    MINIO_ROOT_PASSWORD: str = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
    MINIO_SECURE: bool = False
    
    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

settings = Settings()
