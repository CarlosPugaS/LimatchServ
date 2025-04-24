/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",],
  theme: {
    extend: {
      colors: {
        primario: "#2C3E50",
        secundario: "#A3B18A",
        fondo: "#F6F5F2",
        accion: "#E67E22",
        texto: "#333333",
      },
      fontFamily: {
        barlow: ['"Barlow"', 'sans-serif'],
        ConcertOne: ["Concert One", 'sans-serif'] 
      }
    },
  },
  plugins: [],
}

