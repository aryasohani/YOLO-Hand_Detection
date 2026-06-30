"""
yolo_service.py
Loads YOLOv8 once and provides safe inference.
"""

import logging
import os
from pathlib import Path

import numpy as np
import torch
from ultralytics import YOLO

from app.core.config import settings

logger = logging.getLogger(__name__)

_model = None


# ─────────────────────────────────────────────────────────────
# Model Loader (Singleton)
# ─────────────────────────────────────────────────────────────

def get_model(model_path: str = None):
    global _model

    if _model is not None:
        return _model

    path = Path(model_path) if model_path else Path(settings.MODEL_PATH)

    logger.info("========== YOLO DEBUG ==========")
    logger.info(f"CWD                   : {os.getcwd()}")
    logger.info(f"MODEL_PATH            : {path}")
    logger.info(f"MODEL_EXISTS          : {path.exists()}")
    logger.info(f"Torch version         : {torch.__version__}")

    try:
        from ultralytics import __version__ as uv
        logger.info(f"Ultralytics version   : {uv}")
    except Exception:
        logger.warning("Could not read ultralytics version")

    if not path.exists():
        raise FileNotFoundError(f"Model not found at: {path}")

    logger.info("Loading YOLO model...")

    try:
        _model = YOLO(str(path))
        _model.fuse()  # 🔥 faster inference (important for Render)
        logger.info("✅ YOLO model loaded successfully.")
    except Exception as e:
        logger.exception("❌ YOLO load failed")
        raise e

    logger.info("================================")

    return _model


# ─────────────────────────────────────────────────────────────
# Safe Inference
# ─────────────────────────────────────────────────────────────

def run_inference(frame: np.ndarray, conf_threshold: float = 0.25):
    """
    Run YOLO inference safely on a single frame.
    Returns best detection (highest confidence).
    """

    if frame is None or not isinstance(frame, np.ndarray):
        return _empty_result()

    model = get_model()

    h, w = frame.shape[:2]

    try:
        results = model.predict(
            source=frame,
            conf=conf_threshold,
            verbose=False
        )[0]
    except Exception as e:
        logger.error(f"YOLO inference error: {e}")
        return _empty_result()

    if results.boxes is None or len(results.boxes) == 0:
        return _empty_result()

    # ── FIX: correct confidence selection (IMPORTANT BUG FIX) ──
    confs = results.boxes.conf.cpu().numpy()
    best_idx = int(np.argmax(confs))

    box = results.boxes[best_idx]

    try:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = float(box.conf[0])
    except Exception as e:
        logger.error(f"Box parsing error: {e}")
        return _empty_result()

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2

    return {
        "detected": True,
        "cx_px": round(float(cx), 2),
        "cy_px": round(float(cy), 2),
        "cx_norm": round(float(cx / w), 6),
        "cy_norm": round(float(cy / h), 6),
        "bbox_x1": round(float(x1), 2),
        "bbox_y1": round(float(y1), 2),
        "bbox_x2": round(float(x2), 2),
        "bbox_y2": round(float(y2), 2),
        "confidence": round(conf, 4),
    }


# ─────────────────────────────────────────────────────────────
# Empty fallback (prevents pipeline crash)
# ─────────────────────────────────────────────────────────────

def _empty_result():
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