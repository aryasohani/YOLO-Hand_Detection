"""
schemas/detection.py
Pydantic models for API request validation and response serialisation.
"""

from typing import Optional
from pydantic import BaseModel, Field


# ── Response sub-models ────────────────────────────────────────────────────────

class TrajectoryStats(BaseModel):
    total_frames: int
    detected_frames: int
    detection_pct: float = Field(..., description="Percentage of frames with a detection")
    processing_time: float = Field(..., description="Wall-clock seconds")
    avg_confidence: Optional[float] = None
    x_min: Optional[float] = None
    x_max: Optional[float] = None
    y_min: Optional[float] = None
    y_max: Optional[float] = None
    time_start: Optional[float] = None
    time_end: Optional[float] = None


class DetectionResponse(BaseModel):
    success: bool
    job_id: str
    output_video_url: str
    csv_full_url: str
    csv_clean_url: str
    graph_url: str
    stats: TrajectoryStats


class ResultFilesResponse(BaseModel):
    job_id: str
    files: dict[str, str]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str