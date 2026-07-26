/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ksp: {
          navy: "#0B1F3A",
          blue: "#13315C",
          accent: "#2E6FDB",
          steel: "#8B9BB4",
          surface: "#101826",
        },
      },
    },
  },
  plugins: [],
};
