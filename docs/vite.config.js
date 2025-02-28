import wasm from "vite-plugin-wasm";
import topLevelAwait from "vite-plugin-top-level-await";

/** @type {import("vite").UserConfig} */
const config = {
  plugins: [wasm(), topLevelAwait()],
  optimizeDeps: {
    exclude: process.env.NODE_ENV === "production" ? [] : ["@rerun-io/web-viewer"],
  },
  server: {
    port: 5173,
  },
};



config.base = `/reflex-viz`;


export default config;
