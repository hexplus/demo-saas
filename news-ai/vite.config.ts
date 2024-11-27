import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // Alias '@' points to 'src' folder
    },
    extensions: ['.js', '.ts', '.jsx', '.tsx', '.json'], // Avoid needing to specify extensions
  },
  server: {
    hmr: true, // Esta opción asegura que las rutas no encontradas sean manejadas por React Router
  },
});
