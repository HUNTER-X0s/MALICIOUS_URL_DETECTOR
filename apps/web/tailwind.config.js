/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Core brand
        sentinel: {
          bg: '#030712',
          surface: '#0f1117',
          card: '#141922',
          border: 'rgba(255, 255, 255, 0.06)',
          accent: '#6366f1',
          'accent-light': '#818cf8',
          'accent-glow': 'rgba(99, 102, 241, 0.25)',
          'accent-subtle': 'rgba(99, 102, 241, 0.08)',
        },
        verdict: {
          malicious: '#ef4444',
          'malicious-bg': 'rgba(239, 68, 68, 0.08)',
          'malicious-border': 'rgba(239, 68, 68, 0.25)',
          suspicious: '#f59e0b',
          'suspicious-bg': 'rgba(245, 158, 11, 0.08)',
          'suspicious-border': 'rgba(245, 158, 11, 0.25)',
          benign: '#10b981',
          'benign-bg': 'rgba(16, 185, 129, 0.08)',
          'benign-border': 'rgba(16, 185, 129, 0.25)',
          unknown: '#64748b',
          'unknown-bg': 'rgba(100, 116, 139, 0.1)',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'monospace'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'hero-gradient': 'radial-gradient(ellipse 80% 60% at 50% -10%, rgba(99, 102, 241, 0.15), transparent 70%)',
        'card-shine': 'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 50%)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.4s ease-out forwards',
        'fade-in-up': 'fadeInUp 0.5s ease-out forwards',
        'fade-in-scale': 'fadeInScale 0.4s ease-out forwards',
        'slide-in-right': 'slideInRight 0.4s ease-out forwards',
        'pulse-glow': 'pulseGlow 2.5s ease-in-out infinite',
        'shield-pulse': 'shieldPulse 3s ease-in-out infinite',
        'float': 'float 4s ease-in-out infinite',
        'spin-slow': 'spin 8s linear infinite',
        'ping-slow': 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite',
        'shimmer': 'shimmer 1.5s infinite',
        'orb-drift': 'orbDrift 20s ease-in-out infinite alternate',
        'progress': 'progressIndeterminate 1.4s ease-in-out infinite',
        'scan-pulse': 'scanPulse 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeInUp: {
          '0%':   { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeInScale: {
          '0%':   { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        slideInRight: {
          '0%':   { opacity: '0', transform: 'translateX(-12px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 8px rgba(99,102,241,0.3), 0 0 16px rgba(99,102,241,0.15)' },
          '50%':      { boxShadow: '0 0 16px rgba(99,102,241,0.5), 0 0 32px rgba(99,102,241,0.25)' },
        },
        shieldPulse: {
          '0%, 100%': { transform: 'scale(1)', filter: 'drop-shadow(0 0 8px rgba(99,102,241,0.4))' },
          '50%':      { transform: 'scale(1.04)', filter: 'drop-shadow(0 0 16px rgba(99,102,241,0.6))' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%':      { transform: 'translateY(-6px)' },
        },
        shimmer: {
          '0%':   { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        orbDrift: {
          '0%':   { opacity: '1', transform: 'scale(1) translateY(0)' },
          '50%':  { opacity: '0.8', transform: 'scale(1.05) translateY(-10px)' },
          '100%': { opacity: '1', transform: 'scale(0.98) translateY(5px)' },
        },
        progressIndeterminate: {
          '0%':   { left: '-40%', width: '40%' },
          '60%':  { left: '100%', width: '40%' },
          '100%': { left: '100%', width: '40%' },
        },
        scanPulse: {
          '0%, 100%': { opacity: '0.5', transform: 'scaleX(0.8)' },
          '50%':      { opacity: '1', transform: 'scaleX(1)' },
        },
      },
      backdropBlur: {
        xs: '2px',
        '3xl': '64px',
        '4xl': '80px',
      },
      boxShadow: {
        'glow-sm':     '0 0 8px rgba(99,102,241,0.25)',
        'glow-md':     '0 0 16px rgba(99,102,241,0.3), 0 0 32px rgba(99,102,241,0.15)',
        'glow-lg':     '0 0 32px rgba(99,102,241,0.3), 0 0 64px rgba(99,102,241,0.15)',
        'glow-safe':   '0 0 16px rgba(16,185,129,0.3), 0 0 32px rgba(16,185,129,0.15)',
        'glow-danger': '0 0 16px rgba(239,68,68,0.3), 0 0 32px rgba(239,68,68,0.15)',
        'glow-warn':   '0 0 16px rgba(245,158,11,0.3), 0 0 32px rgba(245,158,11,0.15)',
        'glass':       '0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05)',
        'glass-lg':    '0 20px 60px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.08)',
        'card':        '0 4px 24px rgba(0,0,0,0.4)',
        'card-hover':  '0 8px 40px rgba(0,0,0,0.5), 0 0 20px rgba(99,102,241,0.08)',
      },
      transitionDuration: {
        '250': '250ms',
        '400': '400ms',
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
        '30': '7.5rem',
      },
      maxWidth: {
        '8xl': '88rem',
        '9xl': '96rem',
      },
      zIndex: {
        '60': '60',
        '70': '70',
        '80': '80',
        '90': '90',
        '100': '100',
      },
    },
  },
  plugins: [],
};
