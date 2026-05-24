/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        terminal: {
          bg: '#050A15',      // Deep navy/black
          panel: '#0B132B',   // Slightly lighter for cards
          border: '#1C2A4A',  // Sharp, subtle lines
          cyan: '#00F0FF',    // Primary actions/text
          green: '#00FF41',   // Success/Live metrics
          yellow: '#FFB800',  // Warnings
          red: '#FF003C',     // Critical failures
          dim: '#4A5B7C',     // Inactive text
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      boxShadow: {
        'glow-cyan': '0 0 10px rgba(0, 240, 255, 0.3)',
        'glow-red': '0 0 10px rgba(255, 0, 60, 0.3)',
      }
    },
  },
  plugins: [],
}