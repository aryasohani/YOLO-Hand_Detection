/**
 * components/UploadZone.jsx
 * Drag-and-drop / click-to-browse video upload area.
 */

import { useState, useRef, useCallback } from "react";

const ALLOWED = ["video/mp4", "video/avi", "video/quicktime", "video/x-matroska", "video/webm"];

export default function UploadZone({ onFile, file, disabled }) {
  const [drag, setDrag] = useState(false);
  const inputRef = useRef();

  const handleFile = useCallback((f) => {
    if (!f) return;
    if (!ALLOWED.includes(f.type) && !f.name.match(/\.(mp4|avi|mov|mkv|webm)$/i)) {
      alert("Please upload a video file (mp4, avi, mov, mkv, webm).");
      return;
    }
    onFile(f);
  }, [onFile]);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDrag(false);
    handleFile(e.dataTransfer.files[0]);
  }, [handleFile]);

  return (
    <div
      onClick={() => !disabled && inputRef.current.click()}
      onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
      onDragLeave={() => setDrag(false)}
      onDrop={handleDrop}
      style={{
        border: `2px dashed ${drag ? "#00ff88" : file ? "#00cfff66" : "rgba(255,255,255,0.12)"}`,
        borderRadius: 20,
        padding: "52px 32px",
        textAlign: "center",
        cursor: disabled ? "default" : "pointer",
        transition: "all 0.25s ease",
        background: drag
          ? "rgba(0,255,136,0.04)"
          : file
          ? "rgba(0,207,255,0.04)"
          : "rgba(255,255,255,0.015)",
        position: "relative",
        overflow: "hidden",
        userSelect: "none",
      }}
    >
      {/* Ambient glow */}
      <div style={{
        position: "absolute", width: 240, height: 240, borderRadius: "50%",
        top: -80, left: "50%", transform: "translateX(-50%)",
        background: file
          ? "radial-gradient(circle, rgba(0,207,255,0.07) 0%, transparent 70%)"
          : "radial-gradient(circle, rgba(0,255,136,0.05) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />

      <input
        ref={inputRef}
        type="file"
        accept="video/*"
        style={{ display: "none" }}
        onChange={(e) => handleFile(e.target.files[0])}
      />

      {/* Upload icon */}
      <div style={{ color: file ? "#00cfff" : "#555", marginBottom: 16 }}>
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <polyline points="16 16 12 12 8 16" />
          <line x1="12" y1="12" x2="12" y2="21" />
          <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3" />
        </svg>
      </div>

      {file ? (
        <>
          <p style={{ color: "#e0e0e0", fontWeight: 600, marginBottom: 6, fontSize: 15 }}>
            {file.name}
          </p>
          <p style={{ color: "#666", fontSize: 13 }}>
            {(file.size / 1024 / 1024).toFixed(1)} MB · Click to replace
          </p>
        </>
      ) : (
        <>
          <p style={{ color: "#bbb", fontWeight: 500, marginBottom: 8, fontSize: 15 }}>
            Drop video here or click to browse
          </p>
          <p style={{ color: "#555", fontSize: 13 }}>
            MP4, AVI, MOV, MKV, WEBM · Max 500 MB
          </p>
        </>
      )}
    </div>
  );
}
