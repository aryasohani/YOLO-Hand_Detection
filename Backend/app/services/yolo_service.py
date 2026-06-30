"""
yolo_service.py
Loads the YOLOv8 model once and exposes inference helpers.
"""

import logging
import os
from pathlib import Path

import numpy as np
import torch
from ultralytics import YOLO

from app.core.config import settings

logger = logging.getLogger(__name__)

# Singleton model
_model = None


def get_model(model_path: str = None):
    global _model

    if _model is not None:
        return _model

    path = Path(model_path) if model_path else Path(settings.MODEL_PATH)

    logger.info("========== YOLO DEBUG ==========")
    logger.info(f"Current working directory : {os.getcwd()}")
    logger.info(f"Configured MODEL_PATH     : {settings.MODEL_PATH}")
    logger.info(f"Resolved model path       : {path.resolve()}")
    logger.info(f"Model exists?             : {path.exists()}")
    logger.info(f"Torch version             : {torch.__version__}")

    try:
        from ultralytics import __version__ as uv
        logger.info(f"Ultralytics version       : {uv}")
    except Exception:
        logger.exception("Could not determine Ultralytics version")

    logger.info("Loading YOLO model...")

    try:
        _model = YOLO(str(path))
        logger.info("✅ YOLO model loaded successfully.")
    except Exception:
        logger.exception("❌ Failed to load YOLO model")
        raise

    logger.info("================================")

    return _model


def run_inference(frame: np.ndarray, conf_threshold: float = 0.25):
    """
    Run inference on a single frame.

    Returns a dictionary describing the highest-confidence detection.
    """

    model = get_model()

    height, width = frame.shape[:2]

    results = model.predict(
        source=frame,
        conf=conf_threshold,
        verbose=False,
    )[0]

    if len(results.boxes) == 0:
        return {
            "detected": False,
            "cx_px": None,
            "cy_px": None,
            "cx_norm": None,
            "cy_norm": None,
            "bbox_x1": None,
            "bbox_y1": None,
            "bbox_x2": None,
            "bbox_y2": None,
            "confidence": 0.0,
        }

    best_idx = int(results.boxes.conf.argmax())

    box = results.boxes[best_idx]

    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

    confidence = float(box.conf[0])

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2

    return {
        "detected": True,
        "cx_px": round(float(cx), 2),
        "cy_px": round(float(cy), 2),
        "cx_norm": round(float(cx / width), 6),
        "cy_norm": round(float(cy / height), 6),
        "bbox_x1": round(float(x1), 2),
        "bbox_y1": round(float(y1), 2),
        "bbox_x2": round(float(x2), 2),
        "bbox_y2": round(float(y2), 2),
        "confidence": round(confidence, 4),
    }