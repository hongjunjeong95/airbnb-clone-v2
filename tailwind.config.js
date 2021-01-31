module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      height: {
        18: "4.5rem",
      },
      gridAutoRows: {
        "400px": "minmax(0, 400px)",
      },
      gridTemplateRows: {
        "2-400px": "repeat(2, 400px)",
        "2-200px": "repeat(2, 200px)",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [require("@tailwindcss/line-clamp")],
};
