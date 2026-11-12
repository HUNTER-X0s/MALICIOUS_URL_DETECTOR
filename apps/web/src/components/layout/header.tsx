'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Shield, Lock, ExternalLink, Menu, X, ChevronRight, Puzzle } from 'lucide-react';

export function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const navLinks = [
    { href: '/security', label: 'Security' },
    { href: '/privacy', label: 'Privacy' },
  ];

  return (
    <header
      className={`sticky top-0 z-50 w-full transition-all duration-300 ${
        scrolled
          ? 'border-b border-white/[0.07] bg-[#030712]/90 backdrop-blur-2xl shadow-[0_1px_0_rgba(255,255,255,0.05)]'
          : 'bg-transparent border-b border-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

        {/* ── Brand ── */}
        <Link href="/" className="flex items-center gap-3 group select-none">
          <div className="relative w-9 h-9 flex items-center justify-center">
            {/* Animated glow ring */}
            <div className="absolute inset-0 rounded-xl bg-indigo-500/20 group-hover:bg-indigo-500/30 transition-colors duration-300 animate-pulse-glow" />
            {/* Shield icon */}
            <div className="relative z-10 w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-glow-sm group-hover:shadow-glow-md transition-shadow duration-300">
              <Shield className="w-4.5 h-4.5 text-white" strokeWidth={2.5} style={{ width: '18px', height: '18px' }} />
            </div>
          </div>
          <div className="leading-none">
            <div className="flex items-center gap-2">
              <span className="font-bold text-[1.05rem] text-white tracking-tight">URLSentinel</span>
              <span className="hidden sm:inline text-[9px] uppercase font-bold tracking-widest px-1.5 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                v1.0
              </span>
            </div>
            <p className="text-[10px] text-slate-500 font-mono hidden sm:block mt-0.5">
              Zero-Trust URL Defense
            </p>
          </div>
        </Link>

        {/* ── Desktop Nav ── */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className="px-3 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-white/[0.05] transition-all duration-200 font-medium"
            >
              {label}
            </Link>
          ))}

          <div className="h-5 w-px bg-white/10 mx-2" />

          {/* Live status badge */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/8 border border-emerald-500/20 text-xs font-mono text-emerald-400">
            <span className="live-dot" style={{ width: '7px', height: '7px', borderRadius: '50%', background: '#10b981', display: 'inline-block', position: 'relative' }}>
              <span className="absolute inset-0 rounded-full bg-emerald-500/40 animate-ping" style={{ inset: '-3px' }} />
            </span>
            <span className="font-medium">Engines Active</span>
          </div>

          <div className="h-5 w-px bg-white/10 mx-2" />

          {/* Extension CTA */}
          <a
            href="#extension"
            className="btn-primary text-xs px-4 py-2 flex items-center gap-1.5"
          >
            <Puzzle className="w-3.5 h-3.5" />
            <span>Get Extension</span>
            <ChevronRight className="w-3 h-3 opacity-70" />
          </a>
        </nav>

        {/* ── Mobile Menu Toggle ── */}
        <button
          className="md:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.05] transition-colors"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
          aria-expanded={menuOpen}
        >
          {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* ── Mobile Menu ── */}
      {menuOpen && (
        <div className="md:hidden border-t border-white/[0.07] bg-[#030712]/95 backdrop-blur-2xl animate-fade-in">
          <div className="px-4 py-4 space-y-1">
            {navLinks.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className="block px-3 py-2.5 rounded-lg text-sm text-slate-300 hover:text-white hover:bg-white/[0.05] transition-all"
                onClick={() => setMenuOpen(false)}
              >
                {label}
              </Link>
            ))}
            <div className="pt-3 pb-1">
              <a
                href="#extension"
                className="btn-primary w-full text-sm justify-center"
                onClick={() => setMenuOpen(false)}
              >
                <Puzzle className="w-4 h-4" />
                Get Browser Extension
              </a>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
