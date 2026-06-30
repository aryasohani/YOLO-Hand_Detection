"""
yolo_service.py
Loads the YOLOv8 model once and exposes inference helpers.
"""

import logging
from pathlib import Path

import numpy as np
from ultralytics import YOLO

from app.core.config import settings

logger = logging.getLogger(__name__)

# Singleton model
_model = None


def get_model(model_path: str = None):
    """
    Load and cache the YOLO model.
    """
    global _model

    if _model is not None:
        return _model

    path = Path(model_path) if model_path else Path(settings.MODEL_PATH)

    if not path.exists():
        raise FileNotFoundError(f"Model not found: {path}")

    try:
        logger.info(f"Loading YOLO model from {path}")

        # Load model directly from the .pt file
        _model = YOLO(str(path))

        logger.info("✅ YOLO model loaded successfully.")

    except Exception as e:
        logger.exception(f"❌ Failed to load YOLO model: {e}")
        raise

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