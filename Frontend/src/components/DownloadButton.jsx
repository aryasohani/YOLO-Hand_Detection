/**
 * components/DownloadButton.jsx
 * Opens the file in a NEW TAB instead of downloading in the same tab.
 */

import { resolveUrl } from "../services/api";

const IconOpen = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    <polyline points="15 3 21 3 21 9" />
    <line x1="10" y1="14" x2="21" y2="3" />
  </svg>
);

export default function DownloadButton({ href, label, color = "#00cfff" }) {
  return (
    <a
      href={resolveUrl(href)}
      target="_blank"          
      rel="noopener noreferrer"
      style={{
        display: "inline-flex", alignItems: "center", gap: 8,
        padding: "10px 18px", borderRadius: 10,
        border: `1px solid ${color}44`,
        background: `${color}11`,
        color, fontSize: 13, fontWeight: 500,
        textDecoration: "none",
        transition: "all 0.2s ease",
        fontFamily: "'DM Mono', monospace",
        cursor: "pointer",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.background  = `${color}22`;
        e.currentTarget.style.boxShadow   = `0 0 14px ${color}33`;
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.background  = `${color}11`;
        e.currentTarget.style.boxShadow   = "none";
      }}
    >
      <IconOpen /> {label}
    </a>
  );
}
