/**
 * components/Toast.jsx
 * Fixed-position notification banner.
 */

export default function Toast({ toast }) {
  if (!toast) return null;

  const isError = toast.type === "error";
  const color   = isError ? "#ff8888" : "#00ff88";
  const bg      = isError ? "rgba(255,60,60,0.15)" : "rgba(0,255,136,0.12)";
  const border  = isError ? "rgba(255,60,60,0.3)"  : "rgba(0,255,136,0.3)";
  const shadow  = isError ? "rgba(255,60,60,0.15)" : "rgba(0,255,136,0.15)";

  return (
    <div style={{
      position: "fixed", bottom: 32, right: 32,
      padding: "14px 20px", borderRadius: 12,
      background: bg,
      border: `1px solid ${border}`,
      color,
      fontSize: 13, fontWeight: 500,
      backdropFilter: "blur(12px)",
      animation: "toastIn 0.3s ease",
      zIndex: 100,
      fontFamily: "'DM Mono', monospace",
      boxShadow: `0 8px 32px ${shadow}`,
      maxWidth: 340,
    }}>
      {isError ? "⚠ " : "✓ "}{toast.msg}
    </div>
  );
}
