"""
main.py
FastAPI application entry point.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.detection import router as detection_router
from app.core.config import settings
from app.schemas.detection import HealthResponse

# ──────────────────────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Lifespan
# ──────────────────────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create required directories
    os.makedirs("app/uploads", exist_ok=True)
    os.makedirs("app/outputs", exist_ok=True)

    logger.info(
        f"✅ {settings.APP_TITLE} v{settings.APP_VERSION} started"
    )

    yield

    logger.info(
        f"👋 {settings.APP_TITLE} shutting down"
    )


# ──────────────────────────────────────────────────────────────────────────────
# FastAPI App
# ──────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_TITLE,
    description="YOLOv8-powered hand tracking and trajectory extraction API",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ──────────────────────────────────────────────────────────────────────────────
# CORS
# ──────────────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────────────────────────────
# Static Files
# ──────────────────────────────────────────────────────────────────────────────

app.mount(
    "/outputs",
    StaticFiles(directory="app/outputs"),
    name="outputs",
)

# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────

app.include_router(
    detection_router,
    prefix="/api",
    tags=["Detection"],
)

# ──────────────────────────────────────────────────────────────────────────────
# Root Endpoint
# ──────────────────────────────────────────────────────────────────────────────


@app.get("/")
async def root():
    return {
        "message": "HandTrack AI Backend Running"
    }


# ──────────────────────────────────────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────────────────────────────────────


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
)
async def health_check():

    return HealthResponse(
        status="ok",
        service=settings.APP_TITLE,
        version=settings.APP_VERSION,
    )