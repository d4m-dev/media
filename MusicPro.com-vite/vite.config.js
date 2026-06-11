import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Thay 'ten-repo-cua-ban' bằng tên repository thực tế trên GitHub của bạn
  base: '/MusicPro.com/',
  server: {
    port: 3000
  }
});