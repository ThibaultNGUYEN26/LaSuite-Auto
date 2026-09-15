/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Full URL (protocol + host + port) where the backend is reachable. */
  readonly BACKEND_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
