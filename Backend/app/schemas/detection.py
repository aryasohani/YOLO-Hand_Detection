"""
schemas/detection.py
Pydantic models for API request validation and response serialization.
"""

from typing import Optional, Dict
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# Stats Model
# ─────────────────────────────────────────────────────────────

class TrajectoryStats(BaseModel):
    total_frames: int
    detected_frames: int
    detection_pct: float = Field(..., description="Percentage of frames with detection")
    processing_time: float = Field(..., description="Total processing time in seconds")

    # Optional analytics (safe defaults)
    avg_confidence: Optional[float] = None
    x_min: Optional[float] = None
    x_max: Optional[float] = None
    y_min: Optional[float] = None
    y_max: Optional[float] = None
    time_start: Optional[float] = None
    time_end: Optional[float] = None

    class Config:
        extra = "allow"   # prevents crash if extra keys are passed


# ─────────────────────────────────────────────────────────────
# Main Response Model
# ─────────────────────────────────────────────────────────────

class DetectionResponse(BaseModel):
    success: bool
    job_id: str

    output_video_url: str
    csv_full_url: str
    csv_clean_url: str
    graph_url: str

    stats: TrajectoryStats


# ─────────────────────────────────────────────────────────────
# Results Listing
# ─────────────────────────────────────────────────────────────

class ResultFilesResponse(BaseModel):
    job_id: str
    files: Dict[str, str]   # safer than dict[str, str] for older Python compatibility


# ─────────────────────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str