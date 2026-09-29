import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

/**
 * Vite配置文件
 */
// 后端端口：默认 8080，若本机 8080 被其他程序占用（如 Docker/WSL），
// 启动时可用环境变量覆盖：VITE_BACKEND_PORT=8081 npm run dev
const backendTarget = `http://localhost:${process.env.VITE_BACKEND_PORT || 8080}`

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: backendTarget,
        changeOrigin: true
      },
      '/uploads31': {
        target: backendTarget,
        changeOrigin: true
      }
    }
  }
})
