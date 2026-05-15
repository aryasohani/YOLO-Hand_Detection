"""
trajectory_service.py
Converts raw per-frame detection dicts into CSV files and matplotlib plots.
"""

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — must be set before pyplot import
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def build_dataframe(trajectory: list[dict]) -> pd.DataFrame:
    """Return a DataFrame from raw trajectory list (one row per frame)."""
    return pd.DataFrame(trajectory)


def save_csv(trajectory: list[dict], full_path: str, clean_path: str):
    """
    Write full trajectory CSV and clean (detected-only) CSV.

    Returns:
        (full_path, clean_path, stats_dict)
    """
    df = build_dataframe(trajectory)
    df.to_csv(full_path, index=False)

    clean_df = df[df["detected"]].reset_index(drop=True)
    clean_df.to_csv(clean_path, index=False)

    stats = {}
    if not clean_df.empty:
        stats = {
            "x_min": round(float(clean_df["cx_px"].min()), 2),
            "x_max": round(float(clean_df["cx_px"].max()), 2),
            "y_min": round(float(clean_df["cy_px"].min()), 2),
            "y_max": round(float(clean_df["cy_px"].max()), 2),
            "avg_confidence": round(float(clean_df["confidence"].mean()), 4),
            "time_start": round(float(clean_df["timestamp"].min()), 3),
            "time_end": round(float(clean_df["timestamp"].max()), 3),
        }

    logger.info(f"✅ CSVs saved → {full_path}, {clean_path}")
    return stats


def save_plot(trajectory: list[dict], plot_path: str):
    """
    Generate the 3-panel trajectory analysis figure and save as PNG.
    """
    df = build_dataframe(trajectory)
    clean = df[df["detected"]].reset_index(drop=True)

    if clean.empty:
        logger.warning("No detections — skipping plot generation")
        return

    cx = clean["cx_norm"].values
    cy = clean["cy_norm"].values
    t = clean["timestamp"].values

    fig, axes = plt.subplots(1, 3, figsize=(20, 6), facecolor="#0d0d14")
    for ax in axes:
        ax.set_facecolor("#0d0d14")
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a3d")
        ax.tick_params(colors="#888", labelsize=9)
        ax.xaxis.label.set_color("#aaa")
        ax.yaxis.label.set_color("#aaa")
        ax.title.set_color("#eee")
        ax.grid(True, alpha=0.15, color="#444")

    # ── Plot 1: 2D Spatial Trajectory ────────────────────────────────────────
    ax = axes[0]
    sc = ax.scatter(cx, cy, c=t, cmap="plasma", s=12, zorder=3, alpha=0.85)
    ax.plot(cx, cy, alpha=0.2, color="#888", lw=1, zorder=2)
    ax.scatter(cx[0],  cy[0],  s=140, color="#00ff88", zorder=5, label="Start", marker="^")
    ax.scatter(cx[-1], cy[-1], s=140, color="#ff4466", zorder=5, label="End",   marker="s")
    cbar = plt.colorbar(sc, ax=ax, label="Time (s)")
    cbar.ax.yaxis.label.set_color("#aaa")
    cbar.ax.tick_params(colors="#888")
    ax.set_xlim(0, 1)
    ax.set_ylim(1, 0)
    ax.set_xlabel("X (normalized)")
    ax.set_ylabel("Y (normalized)")
    ax.set_title("2D Hand Trajectory")
    ax.legend(facecolor="#1a1a2e", edgecolor="#333", labelcolor="#ccc", fontsize=8)

    # ── Plot 2: X / Y over Time ──────────────────────────────────────────────
    ax2 = axes[1]
    ax2.plot(t, cx, label="X (norm)", color="#38bdf8", lw=1.5)
    ax2.plot(t, cy, label="Y (norm)", color="#f87171", lw=1.5)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Normalized Position")
    ax2.set_title("X / Y Coordinates over Time")
    ax2.legend(facecolor="#1a1a2e", edgecolor="#333", labelcolor="#ccc", fontsize=8)

    # ── Plot 3: Confidence over Time ─────────────────────────────────────────
    ax3 = axes[2]
    conf = clean["confidence"].values
    ax3.plot(t, conf, color="#fb923c", lw=1.5)
    ax3.axhline(y=0.25, color="#f43f5e", linestyle="--", alpha=0.7, label="Threshold 0.25")
    ax3.fill_between(t, conf, 0.25, where=(conf >= 0.25), alpha=0.18, color="#22c55e")
    ax3.set_ylim(0, 1)
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Confidence Score")
    ax3.set_title("Detection Confidence over Time")
    ax3.legend(facecolor="#1a1a2e", edgecolor="#333", labelcolor="#ccc", fontsize=8)

    plt.suptitle("Hand Trajectory Analysis", fontsize=15, fontweight="bold", color="#fff", y=1.01)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150, bbox_inches="tight", facecolor="#0d0d14")
    plt.close(fig)

    logger.info(f"✅ Plot saved → {plot_path}")