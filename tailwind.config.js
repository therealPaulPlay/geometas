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
    fontSize: {
        xs: '0.75rem',
        sm: '0.8rem',
        base: '0.95rem',
        xl: '1.25rem',
        '2xl': '1.563rem',
        '3xl': '1.953rem',
        '4xl': '2.441rem',
        '5xl': '3.052rem',
    },
    extend: {},
  },
  plugins: [],
}

