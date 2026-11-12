"""Application configuration with Pydantic settings."""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "URLSentinel API"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Security & CORS
    SECRET_KEY: str = "development-secret-key-change-in-production-min-32-chars"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "chrome-extension://*",
    ]

    # Limits
    MAX_URL_LENGTH: int = 2048
    RATE_LIMIT_PER_MINUTE: int = 60

    # Cache & Persistence
    REDIS_ENABLED: bool = True
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL_SECONDS: int = 86400  # 24 hours
    DATABASE_URL: str = "sqlite+aiosqlite:///./urlsentinel.db"

    # Threat Intelligence Feeds
    FEED_REFRESH_INTERVAL_MINUTES: int = 15
    FEED_TIMEOUT_SECONDS: float = 10.0


settings = Settings()
