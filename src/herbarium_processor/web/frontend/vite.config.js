import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import { fileURLToPath, URL } from "node:url";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  build: {
    outDir: "../static/frontend/dist",
    emptyOutDir: true,
    assetsDir: "assets",
  },
  server: {
    port: 5173,
    proxy: {
      // Proxy API during `poetry run dev`
      // Use long timeouts to support slow/long-running backend jobs
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        // Timeouts in ms (http-proxy options). Default is ~120s; we extend it.
        timeout: 5 * 60 * 1000, // 5 minutes for incoming requests
        proxyTimeout: 5 * 60 * 1000, // 5 minutes for outgoing proxy requests
        configure: (proxy) => {
          // Optional: basic error logging to help debug proxy issues
          proxy.on("error", (err, req) => {
            console.error("[vite-proxy]", req.method, req.url, err?.message);
          });
        },
      },
      "/tmp": {
        target: "http://localhost:8000",
        changeOrigin: true,
        timeout: 30 * 60 * 1000,
        proxyTimeout: 30 * 60 * 1000,
      }, // forward the tmp folder... I know it's gross.
    },
  },
});
