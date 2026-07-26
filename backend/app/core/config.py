from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "KSP Crime Intelligence & Analytics Platform"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://ksp_user:ksp_password@db:5432/ksp_crime_db"

    # Redis / Celery
    REDIS_URL: str = "redis://redis:6379/0"

    # JWT
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_USE_ENV_VAR"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000",
                                        "https://ksp-crime-intelligence-platform.vercel.app",
                                        "https://ksp-crime-intelligence-platform-4v3.vercel.app",
                                    ]

    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "ksp_minio_admin"
    MINIO_SECRET_KEY: str = "ksp_minio_password"
    MINIO_BUCKET: str = "ksp-evidence"
    MINIO_SECURE: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
