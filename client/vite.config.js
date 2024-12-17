import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0', // позволяет доступ из внешней сети (не только localhost)
    port: 5173, // убедитесь, что порт совпадает
    proxy:{
      '/api': {
        target: "http://localhost:8000"
      },
      '/admin':{
        target: "http://localhost:8000"
      },
      '/static':{
        target: "http://localhost:8000"
      },
      '/media':{
        target: "http://localhost:8000"
      }
    },
    
  }
})
