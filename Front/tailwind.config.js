/** @type {import('tailwindcss').Config} */

const withMT = require("@material-tailwind/react/utils/withMT");

module.exports = withMT({
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // https://coolors.co/palette/606c38-283618-fefae0-dda15e-bc6c25
        pri: "#283618",
        seg: "#474F59",
        ter: "#dda15e",
        txto: "#fefae0",
        start: "#fefae0",
        end:"#bc6c25",
      },
      fontFamily: {
        barlow: ['"Barlow"', 'sans-serif'],
        ConcertOne: ["Concert One", 'sans-serif'] 
      }
    },
  },
  plugins: [],
}
)
