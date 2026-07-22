import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // FastAPI(8000)와 포트가 겹치지 않도록 5173 고정 (README/CORS 설정과 일치시킨다).
    port: 5173,
  },
})
