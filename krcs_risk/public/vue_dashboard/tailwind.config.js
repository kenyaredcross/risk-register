/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary white-based palette
        'white': '#FFFFFF',
        'off-white': '#FAFAFA',
        'light-gray': '#F5F5F5',

        // Black variants
        'black': '#000000',
        'charcoal': '#1A1A1A',
        'dark-gray': '#2D2D2D',
        'medium-gray': '#666666',
        'light-border': '#E5E5E5',

        // Red accent palette
        'red-primary': '#DC2626', // Vibrant red for critical items
        'red-hover': '#B91C1C',
        'red-light': '#FEE2E2',
        'red-dark': '#991B1B',

        // Risk level colors (with red for critical)
        'risk-low': '#10B981',
        'risk-medium': '#F59E0B',
        'risk-high': '#F97316',
        'risk-critical': '#DC2626',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Poppins', 'sans-serif'],
      },
      boxShadow: {
        'elegant': '0 2px 8px rgba(0, 0, 0, 0.08)',
        'elegant-lg': '0 4px 16px rgba(0, 0, 0, 0.12)',
        'elegant-xl': '0 8px 24px rgba(0, 0, 0, 0.15)',
        'red-glow': '0 0 20px rgba(220, 38, 38, 0.3)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'pulse-red': 'pulseRed 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        pulseRed: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        }
      }
    },
  },
  plugins: [],
}
