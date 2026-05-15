/**
 * hooks/useDetection.js
 * Custom hook that manages the full detection lifecycle:
 *   idle → uploading → processing → done | error
 */

import { useState, useCallback } from "react";
import { detectHands } from "../services/api";

export function useDetection() {
  const [status, setStatus]     = useState("idle");   // idle | uploading | processing | done | error
  const [progress, setProgress] = useState(0);
  const [result, setResult]     = useState(null);
  const [error, setError]       = useState(null);

  const run = useCallback(async (file) => {
    if (!file) return;

    setStatus("uploading");
    setProgress(0);
    setError(null);
    setResult(null);

    try {
      // Real XHR upload progress
      const data = await detectHands(file, (pct) => {
        setProgress(pct);
        if (pct === 100) setStatus("processing");
      });

      setResult(data);
      setStatus("done");
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
  }, []);

  const reset = useCallback(() => {
    setStatus("idle");
    setProgress(0);
    setResult(null);
    setError(null);
  }, []);

  return { status, progress, result, error, run, reset };
}
