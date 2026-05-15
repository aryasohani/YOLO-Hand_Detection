/**
 * components/TrajectoryPlot.jsx
 * Displays the server-generated matplotlib trajectory PNG inline.
 */

import { resolveUrl } from "../services/api";

export default function TrajectoryPlot({ src }) {
  if (!src) return null;

  return (
    <div style={{
      borderRadius: 20,
      overflow: "hidden",
      border: "1px solid rgba(255,255,255,0.07)",
    }}>
      <div style={{
        padding: "14px 20px",
        background: "rgba(255,255,255,0.025)",
        borderBottom: "1px solid rgba(255,255,255,0.06)",
        fontSize: 13, color: "#888",
        display: "flex", alignItems: "center", gap: 8,
      }}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fb923c" strokeWidth="2">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
        </svg>
        Trajectory Analysis Plot
      </div>
      <img
        src={`${resolveUrl(src)}?t=${Date.now()}`}
        alt="Trajectory analysis plot"
        style={{ width: "100%", display: "block" }}
      />
    </div>
  );
}
