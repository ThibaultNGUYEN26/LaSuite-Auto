import { resolve } from 'path'
import { defineConfig } from 'electron-vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  main: {},
  preload: {},
  renderer: {
    // Expose BACKEND_URL (not just the default VITE_ prefix) to the renderer
    // via import.meta.env and to index.html's %BACKEND_URL% interpolation,
    // so the frontend/backend share the same env var name.
    envPrefix: ['VITE_', 'BACKEND_'],
    resolve: {
      alias: {
        '@renderer': resolve('src/renderer/src')
      }
    },
    plugins: [react()]
  }
})
