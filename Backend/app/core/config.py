"""
core/config.py
Centralised settings loaded from environment variables / .env file.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8",extra="ignore")

    # ── Model ────────────────────────────────────────────────────────────────
    MODEL_PATH: str = "best.pt"
    CONF_THRESHOLD: float = 0.25
    TRAIL_LENGTH: int = 30

    # ── Storage ──────────────────────────────────────────────────────────────
    UPLOAD_DIR: str = "app/uploads"
    OUTPUT_DIR: str = "app/outputs"
    MAX_FILE_SIZE_MB: int = 500

    # ── CORS ─────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5177",
        "http://127.0.0.1:5177",
        "https://delicate-valkyrie-8d5e3d.netlify.app"
    ]

    # ── App ──────────────────────────────────────────────────────────────────
    APP_TITLE: str = "HandTrack AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False


settings = Settings()