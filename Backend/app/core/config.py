"""
core/config.py
Centralised settings loaded from environment variables / .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",          # ignores extra env vars Render injects
    )

    # ── Model ────────────────────────────────────────────────────────────────
    MODEL_PATH: str = "models/best.pt"
    CONF_THRESHOLD: float = 0.25
    TRAIL_LENGTH: int = 30

    # ── Storage ──────────────────────────────────────────────────────────────
    UPLOAD_DIR: str = "app/uploads"
    OUTPUT_DIR: str = "app/outputs"
    MAX_FILE_SIZE_MB: int = 500

    # ── CORS ─────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: list[str] = ["*"]

    # ── App ──────────────────────────────────────────────────────────────────
    APP_TITLE: str = "HandTrack AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False


settings = Settings()