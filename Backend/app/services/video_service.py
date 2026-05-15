"""
video_service.py
─────────────────────────────────────────────────────────────────────────────
REAL PATH TRAJECTORY

The trajectory drawn on the video is the EXACT path the hand moved.
- Straight line  → straight line drawn
- Circle motion  → circle drawn
- Oval motion    → oval drawn
- Zigzag motion  → zigzag drawn

No shape fitting. No guessing. Just the real movement, point by point.

Tracking point: FINGERTIP = top-center of the bounding box (most precise).
Smoothing: light moving-average to remove camera jitter (not the shape).
Drawing: the FULL accumulated path is redrawn on EVERY frame so you always
         see the complete shape the hand has traced so far.
"""

import logging
import cv2
import numpy as np
from app.services.yolo_service import run_inference

logger = logging.getLogger(__name__)

# ── Settings ───────────────────────────────────────────────────────────────────
SMOOTH_WINDOW = 5        # light smoothing — removes jitter, keeps real shape
LINE_THICKNESS = 3       # thickness of the trajectory line
BBOX_COLOR     = (0, 255, 128)    # green bounding box


def _get_tip(det: dict):
    """
    Fingertip = top-center of the YOLO bounding box.
    This is the actual tip of the hand/finger pointing up.
    """
    if not det["detected"]:
        return None
    tip_x = int((det["bbox_x1"] + det["bbox_x2"]) / 2)   # center X
    tip_y = int(det["bbox_y1"])                            # TOP of box = fingertip
    return (tip_x, tip_y)


def _smooth(points: list, window: int = SMOOTH_WINDOW) -> list:
    """
    Light moving-average smoothing.
    Only removes camera shake — does NOT change the actual shape of movement.
    Window=5 means each point is averaged with 2 neighbours on each side.
    """
    if len(points) < window:
        return points
    out = []
    for i in range(len(points)):
        lo  = max(0, i - window // 2)
        hi  = min(len(points), i + window // 2 + 1)
        seg = points[lo:hi]
        out.append((
            int(sum(p[0] for p in seg) / len(seg)),
            int(sum(p[1] for p in seg) / len(seg)),
        ))
    return out


def _draw_full_path(frame, points: list):
    """
    Draw the COMPLETE real path of the hand on every frame.

    The path is drawn in two passes:
      Pass 1 — thick dark shadow line  (gives depth / visibility on any background)
      Pass 2 — bright colour gradient  (shows direction: purple → blue → cyan → green)

    The colour gradient tells you WHERE the hand started and where it went.
    Purple = start,  Green = current position.
    """
    if len(points) < 2:
        return

    n = len(points)

    # ── Pass 1: dark shadow (makes path visible on any background) ──────────
    for i in range(1, n):
        cv2.line(frame, points[i-1], points[i],
                 (20, 20, 20), LINE_THICKNESS + 3, cv2.LINE_AA)

    # ── Pass 2: bright gradient line (purple → blue → cyan → green) ─────────
    for i in range(1, n):
        t = i / n    # 0.0 at start → 1.0 at current tip

        # Colour gradient:
        # t=0.0  →  purple   (128,  0, 255)
        # t=0.33 →  blue     (  0, 80, 255)
        # t=0.66 →  cyan     (  0, 220, 255)
        # t=1.0  →  green    (  0, 255, 128)
        if t < 0.33:
            s = t / 0.33
            r = int(128 * (1 - s))
            g = int(80  * s)
            b = 255
        elif t < 0.66:
            s = (t - 0.33) / 0.33
            r = 0
            g = int(80  + 140 * s)
            b = int(255 * (1 - s * 0.3))
        else:
            s = (t - 0.66) / 0.34
            r = 0
            g = int(220 + 35 * s)
            b = int(178 * (1 - s))

        color = (b, g, r)   # OpenCV uses BGR

        # Line gets slightly thicker as it approaches current position
        thickness = max(1, int(LINE_THICKNESS * (0.5 + 0.5 * t)))
        cv2.line(frame, points[i-1], points[i], color, thickness, cv2.LINE_AA)


def _draw_tip_dot(frame, tip: tuple):
    """
    Draw a glowing dot at the current fingertip position.
    Three concentric circles: outer glow → mid ring → bright core.
    """
    cv2.circle(frame, tip, 16, (0,   255, 255),  1, cv2.LINE_AA)   # outer glow
    cv2.circle(frame, tip, 11, (0,   200, 255),  1, cv2.LINE_AA)   # mid ring
    cv2.circle(frame, tip,  6, (0,   255, 128), -1, cv2.LINE_AA)   # filled core
    cv2.circle(frame, tip,  6, (255, 255, 255),  1, cv2.LINE_AA)   # white rim


def _draw_start_dot(frame, pt: tuple):
    """Mark the very first point with a small circle so start is visible."""
    cv2.circle(frame, pt, 8,  (128, 0, 255), -1, cv2.LINE_AA)     # purple fill
    cv2.circle(frame, pt, 8,  (255, 255, 255), 1, cv2.LINE_AA)    # white rim
    cv2.putText(frame, "START", (pt[0] + 10, pt[1] - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 150, 255), 1, cv2.LINE_AA)


def process_video(input_path: str, output_path: str, conf_threshold: float = 0.25):
    """
    Process video frame by frame:

      1.  Run YOLO on every frame
      2.  Extract fingertip position (top-center of bounding box)
      3.  Smooth lightly (remove shake, keep real shape)
      4.  Redraw the FULL accumulated path on every frame
          → the path drawn IS the exact shape the hand moved
      5.  Mark start point (purple dot) and current tip (green glow)
      6.  Draw bounding box and HUD info
      7.  Write to output video

    Returns list[dict] — one per frame — for CSV export.
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {input_path}")

    fps          = cap.get(cv2.CAP_PROP_FPS) or 25
    width        = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height       = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out    = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    trajectory = []   # one dict per frame → CSV
    tip_points = []   # raw tip positions accumulated across all frames
    frame_idx  = 0

    logger.info(f"📹 Real-path trajectory | {total_frames} frames @ {fps:.1f} fps")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        timestamp        = round(frame_idx / fps, 4)
        det              = run_inference(frame, conf_threshold)
        det["frame"]     = frame_idx
        det["timestamp"] = timestamp

        # ── Fingertip ───────────────────────────────────────────────────────
        tip = _get_tip(det)
        if tip:
            tip_points.append(tip)
            det["tip_x"] = tip[0]
            det["tip_y"] = tip[1]
        else:
            det["tip_x"] = None
            det["tip_y"] = None

        trajectory.append(det)

        # ── Smooth and draw ─────────────────────────────────────────────────
        smoothed = _smooth(tip_points)

        # Draw the full real path
        _draw_full_path(frame, smoothed)

        # Mark start point
        if len(smoothed) > 0:
            _draw_start_dot(frame, smoothed[0])

        # Mark current tip
        if tip:
            _draw_tip_dot(frame, tip)

        # ── Bounding box ────────────────────────────────────────────────────
        if det["detected"]:
            x1 = int(det["bbox_x1"])
            y1 = int(det["bbox_y1"])
            x2 = int(det["bbox_x2"])
            y2 = int(det["bbox_y2"])
            cv2.rectangle(frame, (x1, y1), (x2, y2),
                          BBOX_COLOR, 2, cv2.LINE_AA)

            # HUD
            cv2.putText(frame, f"Frame: {frame_idx}",
                        (20, 38), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (255, 255, 255), 2, cv2.LINE_AA)
            if tip:
                cv2.putText(frame, f"Tip  X:{tip[0]}  Y:{tip[1]}",
                            (20, 68), cv2.FONT_HERSHEY_SIMPLEX,
                            0.65, (0, 255, 128), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Conf: {det['confidence']:.2f}",
                        (20, 96), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 200, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Path pts: {len(tip_points)}",
                        (20, 124), cv2.FONT_HERSHEY_SIMPLEX,
                        0.55, (180, 180, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, "No Detection",
                        (20, 38), cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 0, 255), 2, cv2.LINE_AA)

        out.write(frame)
        frame_idx += 1

        if frame_idx % 100 == 0:
            logger.info(
                f"   ↳ {frame_idx}/{total_frames} "
                f"| path pts: {len(tip_points)}"
            )

    cap.release()
    out.release()
    logger.info(
        f"✅ Real-path video saved → {output_path} "
        f"| total path pts: {len(tip_points)}"
    )
    return trajectory