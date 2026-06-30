"""
yolo_service.py
Loads the YOLOv8 model once at startup and exposes inference helpers.
"""

import logging
from pathlib import Path

import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)

# Lazy-loaded singleton
_model = None


def get_model(model_path: str = None):
    """Load and cache the YOLOv8 model (singleton)."""
    global _model
    if _model is None:
        # Use settings.MODEL_PATH if no explicit path given
        path = str(model_path) if model_path else str(settings.MODEL_PATH)
        try:
            from ultralytics import YOLO  # type: ignore
            if not Path(path).exists():
                raise FileNotFoundError(f"Model not found: {path}")
            _model = YOLO(path)
            logger.info(f"✅ YOLOv8 model loaded from {path}")
        except Exception as exc:
            logger.error(f"❌ Failed to load model: {exc}")
            raise
    return _model


def run_inference(frame: np.ndarray, conf_threshold: float = 0.25):
    """
    Run YOLOv8 on a single BGR frame.

    Returns:
        dict with keys: detected, cx_px, cy_px, cx_norm, cy_norm,
                        bbox_x1, bbox_y1, bbox_x2, bbox_y2, confidence
        or None detection dict when nothing found.
    """
    model = get_model()
    height, width = frame.shape[:2]

    results = model(frame, verbose=False, conf=conf_threshold)[0]

    if len(results.boxes) == 0:
        return {
            "detected": False,
            "cx_px": None, "cy_px": None,
            "cx_norm": None, "cy_norm": None,
            "bbox_x1": None, "bbox_y1": None,
            "bbox_x2": None, "bbox_y2": None,
            "confidence": 0.0,
        }

    # Pick highest-confidence detection
    best_idx = results.boxes.conf.argmax()
    box = results.boxes[best_idx]
    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
    conf = float(box.conf[0])

    cx_px = (x1 + x2) / 2
    cy_px = (y1 + y2) / 2

    return {
        "detected": True,
        "cx_px": round(float(cx_px), 2),
        "cy_px": round(float(cy_px), 2),
        "cx_norm": round(cx_px / width, 6),
        "cy_norm": round(cy_px / height, 6),
        "bbox_x1": round(float(x1), 2),
        "bbox_y1": round(float(y1), 2),
        "bbox_x2": round(float(x2), 2),
        "bbox_y2": round(float(y2), 2),
        "confidence": round(conf, 4),
    }