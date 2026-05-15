/**
 * components/StatCard.jsx
 * Single metric card displayed in the analytics grid.
 */

export default function StatCard({ label, value, unit = "", accent = "#e0e0e0" }) {
  return (
    <div style={{
      background: "rgba(255,255,255,0.03)",
      border: "1px solid rgba(255,255,255,0.07)",
      borderRadius: 14,
      padding: "22px 24px",
      display: "flex",
      flexDirection: "column",
      gap: 6,
    }}>
      <span style={{
        fontSize: 11,
        letterSpacing: "0.12em",
        textTransform: "uppercase",
        color: "#555",
        fontFamily: "'DM Mono', monospace",
      }}>
        {label}
      </span>
      <span style={{
        fontSize: 32,
        fontWeight: 700,
        color: accent,
        fontFamily: "'Space Grotesk', sans-serif",
        lineHeight: 1,
      }}>
        {value}
        {unit && (
          <span style={{ fontSize: 15, fontWeight: 400, color: "#555", marginLeft: 4 }}>
            {unit}
          </span>
        )}
      </span>
    </div>
  );
}
