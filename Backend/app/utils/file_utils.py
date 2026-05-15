"""
utils/file_utils.py
File validation, extension checks, and disk cleanup helpers.
"""

import logging
import shutil
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}


def validate_video_extension(filename: str) -> str:
    """
    Return the lowercase extension if allowed, otherwise raise ValueError.
    """
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported format '{ext}'. "
            f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    return ext


def make_job_dirs(upload_dir: str, output_dir: str) -> tuple[str, Path, Path]:
    """
    Create unique upload + output directories for a new job.

    Returns:
        (job_id, upload_path_dir, output_path_dir)
    """
    job_id = str(uuid.uuid4())
    out_dir = Path(output_dir) / job_id
    out_dir.mkdir(parents=True, exist_ok=True)
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    return job_id, Path(upload_dir), out_dir


def cleanup_job(upload_path: Path, output_dir: Path) -> None:
    """Remove upload file and output directory for a job (e.g. on error)."""
    try:
        if upload_path.exists():
            upload_path.unlink()
        if output_dir.exists():
            shutil.rmtree(output_dir)
    except Exception as exc:
        logger.warning(f"Cleanup failed: {exc}")