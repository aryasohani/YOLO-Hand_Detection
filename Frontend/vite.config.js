import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "https://yolo-hand-detection-backend01.onrender.com",
      "/outputs": "https://yolo-hand-detection-backend01.onrender.com",
    },
  },
});
