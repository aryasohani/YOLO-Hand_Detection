/**
 * services/api.js
 * Centralised API calls to the FastAPI backend.
 */

const API_BASE =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

/**
 * Convert backend relative paths into full URLs
 * Example:
 * /outputs/abc/video.mp4
 * ->
 * http://127.0.0.1:8000/outputs/abc/video.mp4
 */
export const resolveUrl = (path) => {
  if (!path) return "";

  // Already absolute URL
  if (path.startsWith("http")) {
    return path;
  }

  return `${API_BASE}${path}`;
};

/**
 * Upload video and run hand detection
 */
export async function detectHands(file, onProgress) {
  return new Promise((resolve, reject) => {
    const form = new FormData();

    form.append("file", file);

    const xhr = new XMLHttpRequest();

    // Upload progress
    xhr.upload.addEventListener("progress", (e) => {
      if (e.lengthComputable && onProgress) {
        const percent = Math.round(
          (e.loaded / e.total) * 100
        );

        onProgress(percent);
      }
    });

    // Request completed
    xhr.addEventListener("load", () => {
      try {
        const data = JSON.parse(xhr.responseText);

        if (xhr.status >= 200 && xhr.status < 300) {

          // Convert all backend paths to full URLs
          data.output_video_url = resolveUrl(
            data.output_video_url
          );

          data.csv_full_url = resolveUrl(
            data.csv_full_url
          );

          data.csv_clean_url = resolveUrl(
            data.csv_clean_url
          );

          data.graph_url = resolveUrl(
            data.graph_url
          );

          resolve(data);

        } else {
          reject(
            new Error(
              data.detail || `Server error ${xhr.status}`
            )
          );
        }

      } catch (err) {
        reject(
          new Error("Invalid server response")
        );
      }
    });

    // Network error
    xhr.addEventListener("error", () => {
      reject(new Error("Network error"));
    });

    // Abort
    xhr.addEventListener("abort", () => {
      reject(new Error("Upload aborted"));
    });

    // Send request
    xhr.open("POST", `${API_BASE}/api/detect`);

    xhr.send(form);
  });
}

/**
 * Fetch previous job results
 */
export async function getJobResults(jobId) {

  const res = await fetch(
    `${API_BASE}/api/results/${jobId}`
  );

  if (!res.ok) {
    throw new Error(`Job not found: ${jobId}`);
  }

  const data = await res.json();

  // Resolve URLs
  data.output_video_url = resolveUrl(
    data.output_video_url
  );

  data.csv_full_url = resolveUrl(
    data.csv_full_url
  );

  data.csv_clean_url = resolveUrl(
    data.csv_clean_url
  );

  data.graph_url = resolveUrl(
    data.graph_url
  );

  return data;
}

/**
 * Backend health check
 */
export async function checkHealth() {

  try {
    const res = await fetch(
      `${API_BASE}/health`
    );

    return res.ok;

  } catch {
    return false;
  }
}

export default {
  detectHands,
  getJobResults,
  checkHealth,
  resolveUrl,
};