/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./destinations/**/*.html",
    "./yachts/**/*.html",
    "./js/*.js",
  ],
  safelist: [
    { pattern: /^(bg|text|border)-(cream|navy|teal|coral)(\/\d+)?$/ },
  ],
  theme: {
    extend: {
      colors: {
        cream: "#F7F6F1",
        navy: "#102C3A",
        teal: "#0D7779",
        coral: "#E3836E",
      },
    },
  },
  plugins: [],
};
