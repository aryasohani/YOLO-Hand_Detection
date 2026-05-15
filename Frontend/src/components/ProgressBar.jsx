/**
 * components/ProgressBar.jsx
 * Animated progress bar with optional label.
 */

export default function ProgressBar({ value, label, sublabel }) {
  return (
    <div style={{ width: "100%" }}>
      {(label || sublabel) && (
        <div style={{
          display: "flex", justifyContent: "space-between",
          marginBottom: 8, fontSize: 12,
          color: "#666", fontFamily: "'DM Mono', monospace",
        }}>
          <span style={{ animation: "pulse 1.5s infinite" }}>{label}</span>
          <span>{sublabel}</span>
        </div>
      )}
      <div style={{
        width: "100%", height: 4,
        background: "rgba(255,255,255,0.08)",
        borderRadius: 2, overflow: "hidden",
      }}>
        <div style={{
          height: "100%",
          width: `${value}%`,
          background: "linear-gradient(90deg, #00ff88, #00cfff)",
          borderRadius: 2,
          transition: "width 0.3s ease",
          boxShadow: "0 0 12px #00ff8866",
        }} />
      </div>
    </div>
  );
}
