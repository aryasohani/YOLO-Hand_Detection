/**
 * components/VideoPlayer.jsx
 * Dark-themed native video player for displaying annotated output.
 */

import { resolveUrl } from "../services/api";

export default function VideoPlayer({ src, title = "Output Video" }) {
  if (!src) return null;

  return (
    <div style={{
      borderRadius: 20,
      overflow: "hidden",
      border: "1px solid rgba(255,255,255,0.07)",
    }}>
      {/* Header bar */}
      <div style={{
        padding: "14px 20px",
        background: "rgba(255,255,255,0.025)",
        borderBottom: "1px solid rgba(255,255,255,0.06)",
        fontSize: 13, color: "#888",
        display: "flex", alignItems: "center", gap: 8,
      }}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00cfff" strokeWidth="2">
          <polygon points="23 7 16 12 23 17 23 7" />
          <rect x="1" y="5" width="15" height="14" rx="2" ry="2" />
        </svg>
        {title}
      </div>

      <video
        controls
        style={{ width: "100%", display: "block", background: "#000", maxHeight: 520 }}
        src={resolveUrl(src)}
      />
    </div>
  );
}
