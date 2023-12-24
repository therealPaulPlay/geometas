/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'templates/**/*.html',
    'quiz/**/*.html',
    'geobin/**/*.html',
    'accounts/**/*.html',
    'cms/**/*.html',
    'articles/**/*.html',
  ],
  theme: {
    fontFamily: {
        'sans': ['Rubik', 'ui-sans-serif', 'system-ui', 'sans-serif', "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"],
    },
    extend: {},
  },
  plugins: [],
}

