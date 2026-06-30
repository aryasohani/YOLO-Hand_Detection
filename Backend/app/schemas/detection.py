"""
api/routes/detection.py
Endpoints:
POST /api/detect
GET  /api/results/{job_id}
"""

import logging
import time
import traceback
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.schemas.detection import DetectionResponse, ResultFilesResponse
from app.services.trajectory_service import save_csv, save_plot
from app.services.video_service import process_video
from app.utils.file_utils import (
    cleanup_job,
    make_job_dirs,
    validate_video_extension,
)

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024


@router.post(
    "/detect",
    response_model=DetectionResponse,
    summary="Detect hands in uploaded video",
)
async def detect(
    file: UploadFile = File(
        ..., description="Video file (mp4/avi/mov/mkv/webm)"
    )
):

    try:
        ext = validate_video_extension(file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    content = await file.read()

    if len(content) > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max allowed: {settings.MAX_FILE_SIZE_MB} MB",
        )

    job_id, upload_dir, output_dir = make_job_dirs(
        settings.UPLOAD_DIR,
        settings.OUTPUT_DIR,
    )

    input_path = upload_dir / f"{job_id}{ext}"

    with open(input_path, "wb") as f:
        f.write(content)

    logger.info(
        f"📥 Job {job_id} | {file.filename} | {len(content)/1024/1024:.2f} MB"
    )

    output_video = output_dir / "output_trajectory.mp4"
    full_csv = output_dir / "trajectory_full.csv"
    clean_csv = output_dir / "trajectory_clean.csv"
    plot_png = output_dir / "trajectory_plot.png"

    start = time.time()

    try:

        trajectory = process_video(
            str(input_path),
            str(output_video),
            conf_threshold=settings.CONF_THRESHOLD,
        )

        stats = save_csv(
            trajectory,
            str(full_csv),
            str(clean_csv),
        )

        save_plot(
            trajectory,
            str(plot_png),
        )

    except Exception as exc:

        logger.exception(f"❌ Job {job_id} failed")

        cleanup_job(
            input_path,
            output_dir,
        )

        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {exc}",
        )

    processing_time = round(time.time() - start, 2)

    total_frames = len(trajectory)

    detected_frames = sum(
        1 for frame in trajectory if frame["detected"]
    )

    detection_pct = (
        round(detected_frames * 100 / total_frames, 1)
        if total_frames
        else 0
    )

    base = f"/outputs/{job_id}"

    return DetectionResponse(
        success=True,
        job_id=job_id,
        output_video_url=f"{base}/output_trajectory.mp4",
        csv_full_url=f"{base}/trajectory_full.csv",
        csv_clean_url=f"{base}/trajectory_clean.csv",
        graph_url=f"{base}/trajectory_plot.png",
        stats={
            "total_frames": total_frames,
            "detected_frames": detected_frames,
            "detection_pct": detection_pct,
            "processing_time": processing_time,
            **stats,
        },
    )


@router.get(
    "/results/{job_id}",
    response_model=ResultFilesResponse,
    summary="List output files",
)
async def get_result(job_id: str):

    output_dir = Path(settings.OUTPUT_DIR) / job_id

    if not output_dir.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Job '{job_id}' not found",
        )

    base = f"/outputs/{job_id}"

    files = {
        f.name: f"{base}/{f.name}"
        for f in output_dir.iterdir()
        if f.is_file()
    }

    return ResultFilesResponse(
        job_id=job_id,
        files=files,
    )