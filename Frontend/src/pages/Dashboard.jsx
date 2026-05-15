/**
 * pages/Dashboard.jsx
 * Main page — composes upload, progress, analytics, video, and downloads.
 */

import { useState } from "react";
import { useDetection }    from "../hooks/useDetection";
import { useToast }        from "../hooks/useToast";
import UploadZone          from "../components/UploadZone";
import ProgressBar         from "../components/ProgressBar";
import AnalyticsPanel      from "../components/AnalyticsPanel";
import VideoPlayer         from "../components/VideoPlayer";
import TrajectoryPlot      from "../components/TrajectoryPlot";
import DownloadButton      from "../components/DownloadButton";
import Toast               from "../components/Toast";

const IconScan = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2" />
    <rect x="7" y="7" width="10" height="10" rx="1" />
  </svg>
);
const IconCheck = () => (
  <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

export default function Dashboard() {
  const [file, setFile]                   = useState(null);
  const { status, progress, result, error, run, reset } = useDetection();
  const { toast, show: showToast }        = useToast();

  const handleAnalyze = async () => {
    if (!file) return;
    await run(file);
    if (status !== "error") showToast("Analysis complete!");
  };

  // Show error toast when it surfaces
  if (error && toast?.msg !== error) showToast(error, "error");

  const busy  = status === "uploading" || status === "processing";
  const stats = result?.stats;

  return (
    <div style={{ maxWidth: 960, margin: "0 auto", padding: "56px 24px 0" }}>

      {/* Hero */}
      <div style={{ textAlign: "center", marginBottom: 56 }}>
        <h1 style={{
          fontFamily: "'Space Grotesk', sans-serif",
          fontSize: "clamp(30px, 5vw, 50px)",
          fontWeight: 700,
          letterSpacing: "-0.03em",
          lineHeight: 1.1,
          marginBottom: 16,
          background: "linear-gradient(135deg, #fff 40%, #00ff88)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
        }}>
          Hand Detection &<br />Trajectory Tracking
        </h1>
        <p style={{ color: "#666", fontSize: 16, maxWidth: 480, margin: "0 auto", lineHeight: 1.7 }}>
          Upload any video. YOLOv8 detects hands frame-by-frame, extracts trajectory data,
          and generates annotated outputs.
        </p>
      </div>

      {/* ── Upload card ───────────────────────────────────────────────────── */}
      <div style={{
        background: "rgba(255,255,255,0.025)",
        border: "1px solid rgba(255,255,255,0.07)",
        borderRadius: 24, padding: 32, marginBottom: 32,
        animation: "slideUp 0.5s ease",
      }}>
        <h2 style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 17, fontWeight: 600, marginBottom: 24, color: "#ccc" }}>
          Upload Video
        </h2>

        <UploadZone onFile={setFile} file={file} disabled={busy} />

        {busy && (
          <div style={{ marginTop: 24 }}>
            <ProgressBar
              value={progress}
              label={status === "uploading" ? "⬆ Uploading…" : "⚙ Running inference…"}
              sublabel={`${Math.round(progress)}%`}
            />
            {status === "processing" && (
              <div style={{
                position: "relative", height: 2, marginTop: 16,
                overflow: "hidden", borderRadius: 1,
                background: "rgba(255,255,255,0.04)",
              }}>
                <div className="scan-line" />
              </div>
            )}
          </div>
        )}

        {/* CTA button */}
        <button
          onClick={handleAnalyze}
          disabled={!file || busy}
          style={{
            marginTop: 24, width: "100%", padding: "16px",
            borderRadius: 14, border: "none",
            background: !file || busy
              ? "rgba(255,255,255,0.06)"
              : "linear-gradient(135deg, #00ff88, #00cfff)",
            color: !file || busy ? "#444" : "#080810",
            fontSize: 15, fontWeight: 700,
            cursor: !file || busy ? "not-allowed" : "pointer",
            display: "flex", alignItems: "center", justifyContent: "center", gap: 10,
            transition: "all 0.2s ease",
            fontFamily: "'Space Grotesk', sans-serif",
            letterSpacing: "-0.01em",
            boxShadow: !file || busy ? "none" : "0 0 24px #00ff8844",
          }}
        >
          {busy ? (
            <>
              <div style={{
                width: 18, height: 18, border: "2px solid #555",
                borderTopColor: "#00ff88", borderRadius: "50%",
                animation: "spin 0.8s linear infinite",
              }} />
              Analyzing…
            </>
          ) : (
            <><IconScan /> Analyze Video</>
          )}
        </button>

        {error && (
          <div style={{
            marginTop: 16, padding: "12px 16px", borderRadius: 10,
            background: "rgba(255,60,60,0.08)", border: "1px solid rgba(255,60,60,0.2)",
            color: "#ff6b6b", fontSize: 13, fontFamily: "'DM Mono', monospace",
          }}>
            ⚠ {error}
          </div>
        )}
      </div>

      {/* ── Results ───────────────────────────────────────────────────────── */}
      {result && (
        <div style={{ animation: "slideUp 0.6s ease" }}>

          {/* Success banner */}
          <div style={{
            display: "flex", alignItems: "center", gap: 12,
            padding: "14px 20px", borderRadius: 14,
            background: "rgba(0,255,136,0.07)", border: "1px solid rgba(0,255,136,0.2)",
            marginBottom: 28, color: "#00ff88", fontSize: 14, fontWeight: 500,
          }}>
            <IconCheck />
            Analysis complete — {stats?.detected_frames} hands detected across {stats?.total_frames} frames
          </div>

          {/* Analytics */}
          <div style={{ marginBottom: 28 }}>
            <AnalyticsPanel stats={stats} />
          </div>

          {/* Trajectory plot */}
          <div style={{ marginBottom: 28 }}>
            <TrajectoryPlot src={result.graph_url} />
          </div>

          {/* Annotated video */}
          <div style={{ marginBottom: 28 }}>
            <VideoPlayer src={result.output_video_url} title="Annotated Output Video" />
          </div>

          {/* Downloads */}
          <div style={{
            padding: "24px 28px", borderRadius: 20,
            background: "rgba(255,255,255,0.025)",
            border: "1px solid rgba(255,255,255,0.07)",
            marginBottom: 40,
          }}>
            <h3 style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 15, fontWeight: 600, marginBottom: 16, color: "#ccc" }}>
              Download Results
            </h3>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
              <DownloadButton href={result.output_video_url} label="Annotated Video (.mp4)"  color="#00cfff" />
              <DownloadButton href={result.csv_clean_url}    label="Clean Trajectory (.csv)"  color="#00ff88" />
              <DownloadButton href={result.csv_full_url}     label="Full Trajectory (.csv)"   color="#a78bfa" />
              <DownloadButton href={result.graph_url}        label="Trajectory Plot (.png)"   color="#fb923c" />
            </div>
          </div>
        </div>
      )}

      <Toast toast={toast} />
    </div>
  );
}
