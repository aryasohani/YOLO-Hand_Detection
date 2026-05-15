/**
 * components/AnalyticsPanel.jsx
 * Renders stat cards and coordinate range bars from detection results.
 */

import StatCard from "./StatCard";

const fmt = (n, d = 1) => (n == null ? "—" : Number(n).toFixed(d));

export default function AnalyticsPanel({ stats }) {
  if (!stats) return null;

  return (
    <div>
      {/* Stat grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))",
        gap: 14,
        marginBottom: 20,
      }}>
        <StatCard label="Total Frames"    value={stats.total_frames ?? "—"}            accent="#e0e0e0" />
        <StatCard label="Detected Frames" value={stats.detected_frames ?? "—"}         accent="#00ff88" />
        <StatCard label="Detection Rate"  value={fmt(stats.detection_pct)}  unit="%"   accent="#00cfff" />
        <StatCard label="Process Time"    value={fmt(stats.processing_time, 2)} unit="s" accent="#fb923c" />
        <StatCard label="Avg Confidence"  value={fmt(stats.avg_confidence, 3)}          accent="#a78bfa" />
      </div>

      {/* Coordinate ranges */}
      {stats.x_min != null && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          {[
            { label: "X Range", v: `${fmt(stats.x_min, 0)} → ${fmt(stats.x_max, 0)} px`, color: "#38bdf8" },
            { label: "Y Range", v: `${fmt(stats.y_min, 0)} → ${fmt(stats.y_max, 0)} px`, color: "#f87171" },
          ].map(({ label, v, color }) => (
            <div key={label} style={{
              padding: "16px 20px", borderRadius: 14,
              background: "rgba(255,255,255,0.025)",
              border: "1px solid rgba(255,255,255,0.06)",
            }}>
              <div style={{
                fontSize: 11, color: "#555",
                letterSpacing: "0.1em", textTransform: "uppercase",
                marginBottom: 6, fontFamily: "'DM Mono', monospace",
              }}>
                {label}
              </div>
              <div style={{ color, fontSize: 18, fontWeight: 600, fontFamily: "'DM Mono', monospace" }}>
                {v}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
