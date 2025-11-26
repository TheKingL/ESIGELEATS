/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./static/**/*.js", "./**/*.py"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Palette principale (vert ESIGELEATS)
        primary: {
          50:  "#F3FAF7",
          100: "#E6F4EE",
          200: "#C1E7D6",
          300: "#9DDAC0",
          400: "#6DC6A1",
          500: "#3BB283",
          600: "#289B73",
          700: "#007E6E",
          800: "#005A4D",
          900: "#003B32",
        },

        // Version crème
        cream: "#F5E9D3",

        // Surfaces
        surface: {
          light: "#FFFFFF",
          soft: "#F5E9D3",
          dark: "#0B1020",
        },

        // Background
        background: {
          light: "#FDF8EC",
          dark: "#020617",
        },

        // Textes
        ink: {
          DEFAULT: "#111827",
          soft: "#6B7280",
          lighter: "#9CA3AF",
          inverted: "#F9FAFB",
        },

        black: "#020617",
        white: "#FFFFFF",
      },

      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Poppins", "system-ui", "sans-serif"],
      },

      container: {
        center: true,
        padding: "1rem",
        screens: {
          sm: "640px",
          md: "768px",
          lg: "1024px",
          xl: "1280px",
          "2xl": "1440px",
        },
      },
    },
  },
  plugins: [],
}
