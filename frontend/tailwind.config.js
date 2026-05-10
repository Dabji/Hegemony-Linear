/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Inter", "ui-sans-serif", "system-ui"],
      },
      colors: {
        coal: "#101113",
        iron: "#1a1d21",
        ember: "#e5484d",
        civic: "#f4c95d",
        mint: "#4fd1a5",
        signal: "#58a6ff",
      },
    },
  },
  plugins: [],
};
