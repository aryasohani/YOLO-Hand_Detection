/**
 * App.jsx
 * App shell — global styles, header, font imports, and page mount.
 */

import { useEffect, useState } from "react";
import Dashboard from "./pages/Dashboard";
import { checkHealth } from "./services/api";

export default function App() {
  const [apiOnline, setApiOnline] = useState(null); // null = checking

  useEffect(() => {
    checkHealth()
      .then(setApiOnline)
      .catch(() => setApiOnline(false));
  }, []);

  return (
    <div style={{ minHeight: "100vh", background: "#080810", color: "#e0e0e0", fontFamily: "'Inter', sans-serif" }}>

      {/* Global styles */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #080810; }
        ::-webkit-scrollbar { width: 6px; background: #111; }
        ::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 3px; }
        @keyframes spin    { to { transform: rotate(360deg); } }
        @keyframes pulse   { 0%,100%{opacity:1} 50%{opacity:0.45} }
        @keyframes slideUp { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:translateY(0)} }
        @keyframes toastIn { from{opacity:0;transform:translateX(36px)} to{opacity:1;transform:translateX(0)} }
        .scan-line {
          position: absolute; width: 100%; height: 2px;
          background: linear-gradient(90deg, transparent, #00ff88, transparent);
          animation: scanMove 2.4s linear infinite;
        }
        @keyframes scanMove {
          0%  { top:0;    opacity: 0 }
          8%  { opacity: 1 }
          92% { opacity: 1 }
          100%{ top:100%; opacity: 0 }
        }
      `}</style>

      {/* Header */}
      <header style={{
        borderBottom: "1px solid rgba(255,255,255,0.06)",
        padding: "18px 48px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        background: "rgba(255,255,255,0.015)",
        backdropFilter: "blur(12px)",
        position: "sticky", top: 0, zIndex: 50,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: "linear-gradient(135deg, #00ff88, #00cfff)",
            display: "flex", alignItems: "center", justifyContent: "center",
            boxShadow: "0 0 20px #00ff8855", fontSize: 18,
          }}>✋</div>
          <div>
            <div style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 700, fontSize: 18, letterSpacing: "-0.02em" }}>
              HandTrack AI
            </div>
            <div style={{ fontSize: 11, color: "#555", fontFamily: "'DM Mono', monospace" }}>
              YOLOv8 · Trajectory Analysis
            </div>
          </div>
        </div>

        <div style={{
          display: "flex", alignItems: "center", gap: 8,
          padding: "6px 14px", borderRadius: 20,
          background: apiOnline === false ? "rgba(255,60,60,0.08)" : "rgba(0,255,136,0.08)",
          border: `1px solid ${apiOnline === false ? "rgba(255,60,60,0.2)" : "rgba(0,255,136,0.2)"}`,
          fontSize: 12,
          color: apiOnline === false ? "#ff6b6b" : "#00ff88",
          fontFamily: "'DM Mono', monospace",
        }}>
          <span style={{
            width: 6, height: 6, borderRadius: "50%", display: "inline-block",
            background: apiOnline === false ? "#ff6b6b" : "#00ff88",
            boxShadow: apiOnline === false ? "0 0 6px #ff6b6b" : "0 0 6px #00ff88",
            animation: apiOnline === null ? "pulse 1.2s infinite" : "none",
          }} />
          {apiOnline === null ? "Connecting…" : apiOnline ? "API Online" : "API Offline"}
        </div>
      </header>

      <Dashboard />
    </div>
  );
}
