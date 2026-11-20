'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Search, Clipboard, ArrowRight, AlertCircle, Loader2, Zap, Shield, Globe } from 'lucide-react';

interface UrlInputProps {
  onScan: (url: string) => void;
  isLoading: boolean;
  loadingStep?: string;
}

const SCAN_STAGES = [
  { icon: Shield, label: 'SSRF boundary validation & IP literal screening', color: '#6366f1' },
  { icon: Zap,    label: 'Lexical decomposition & Shannon entropy analysis', color: '#8b5cf6' },
  { icon: Globe,  label: 'Threat intelligence feed correlation & ML scoring', color: '#10b981' },
];

const SAMPLE_URLS = [
  { label: 'Phishing Lure', url: 'https://paypa1-security-verification.com/login', color: 'text-rose-400 border-rose-500/20 hover:bg-rose-500/5' },
  { label: 'IP Anomaly',    url: 'http://45.33.32.156/update/account',            color: 'text-amber-400 border-amber-500/20 hover:bg-amber-500/5' },
  { label: 'Clean Domain',  url: 'https://github.com/security',                   color: 'text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/5' },
];

export function UrlInput({ onScan, isLoading, loadingStep }: UrlInputProps) {
  const [inputUrl, setInputUrl] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [focused, setFocused] = useState(false);
  const [stageIdx, setStageIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const stageTimer = useRef<ReturnType<typeof setInterval> | null>(null);

  // Cycle through scan stage labels while loading
  useEffect(() => {
    if (isLoading) {
      setStageIdx(0);
      stageTimer.current = setInterval(() => {
        setStageIdx(i => (i + 1) % SCAN_STAGES.length);
      }, 1200);
    } else {
      if (stageTimer.current) clearInterval(stageTimer.current);
    }
    return () => { if (stageTimer.current) clearInterval(stageTimer.current); };
  }, [isLoading]);

  const handlePaste = useCallback(async () => {
    try {
      const text = await navigator.clipboard.readText();
      const trimmed = text.trim();
      setInputUrl(trimmed);
      setError(null);
      if (trimmed) inputRef.current?.focus();
    } catch {
      // Clipboard access denied — silent fail
    }
  }, []);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = inputUrl.trim();
    if (!trimmed) {
      setError('Enter a URL to analyze');
      inputRef.current?.focus();
      return;
    }
    setError(null);
    onScan(trimmed);
  }, [inputUrl, onScan]);

  const handleSample = useCallback((url: string) => {
    setInputUrl(url);
    setError(null);
    onScan(url);
  }, [onScan]);

  const stage = SCAN_STAGES[stageIdx];
  const StageIcon = stage.icon;

  return (
    <div className="w-full max-w-3xl mx-auto">
      {/* Main omnibox */}
      <form onSubmit={handleSubmit}>
        <div
          className={`relative rounded-2xl transition-all duration-300 ${
            focused
              ? 'border border-indigo-500/30 shadow-glow-md'
              : 'border border-white/[0.08] shadow-glass'
          } ${isLoading ? 'border-indigo-500/20' : ''}`}
          style={{ background: 'rgba(15,17,23,0.75)', backdropFilter: 'blur(24px)' }}
        >
          {/* Scanning progress bar at top */}
          {isLoading && (
            <div className="absolute top-0 left-0 right-0 h-[2px] rounded-t-2xl overflow-hidden">
              <div
                className="absolute h-full animate-progress"
                style={{
                  background: `linear-gradient(90deg, transparent, ${stage.color}, transparent)`,
                  width: '40%',
                }}
              />
            </div>
          )}

          <div className="flex items-center px-2 py-2">
            {/* Left icon */}
            <div className="pl-3 pr-2 flex-shrink-0">
              {isLoading ? (
                <Loader2
                  className="w-5 h-5 animate-spin"
                  style={{ color: stage.color }}
                />
              ) : (
                <Search className={`w-5 h-5 transition-colors duration-200 ${focused ? 'text-indigo-400' : 'text-slate-500'}`} />
              )}
            </div>

            {/* Text input */}
            <input
              ref={inputRef}
              type="text"
              value={inputUrl}
              onChange={e => { setInputUrl(e.target.value); if (error) setError(null); }}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              placeholder="Paste any URL to analyze — phishing, malware, redirects..."
              disabled={isLoading}
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck={false}
              className="flex-1 bg-transparent text-white placeholder-slate-600 text-sm sm:text-[0.95rem] outline-none py-3.5 px-2 font-mono disabled:opacity-60 min-w-0"
              aria-label="URL to scan"
            />

            {/* Right controls */}
            <div className="flex items-center gap-2 pr-2 flex-shrink-0">
              {/* Paste button — shown when input empty */}
              {!inputUrl && !isLoading && (
                <button
                  type="button"
                  onClick={handlePaste}
                  className="hidden sm:flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white/[0.04] hover:bg-white/[0.07] border border-white/[0.07] text-xs font-mono text-slate-400 hover:text-slate-200 transition-all duration-200"
                  title="Paste from clipboard (Ctrl+V)"
                >
                  <Clipboard className="w-3.5 h-3.5" />
                  Paste
                </button>
              )}

              {/* Analyze button */}
              <button
                type="submit"
                disabled={isLoading || !inputUrl.trim()}
                className="flex items-center gap-2 px-5 sm:px-6 py-3 rounded-xl font-semibold text-sm text-white transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed active:scale-[0.97] select-none"
                style={{
                  background: isLoading
                    ? 'rgba(99,102,241,0.3)'
                    : 'linear-gradient(135deg, #6366f1, #4f46e5)',
                  boxShadow: isLoading ? 'none' : '0 4px 20px rgba(99,102,241,0.35)',
                }}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="hidden sm:inline">Scanning</span>
                  </>
                ) : (
                  <>
                    <span>Analyze</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Animated scanning stage indicator */}
        {isLoading && (
          <div className="mt-4 animate-fade-in">
            <div className="flex items-center gap-3 justify-center">
              {/* Stage icons */}
              <div className="flex items-center gap-2">
                {SCAN_STAGES.map((s, i) => {
                  const Icon = s.icon;
                  return (
                    <div
                      key={i}
                      className="flex items-center justify-center w-7 h-7 rounded-lg transition-all duration-500"
                      style={{
                        background: i === stageIdx ? `${s.color}22` : 'rgba(255,255,255,0.03)',
                        border: `1px solid ${i === stageIdx ? s.color + '55' : 'rgba(255,255,255,0.06)'}`,
                        transform: i === stageIdx ? 'scale(1.1)' : 'scale(1)',
                      }}
                    >
                      <Icon
                        className="w-3.5 h-3.5"
                        style={{ color: i === stageIdx ? s.color : '#475569' }}
                      />
                    </div>
                  );
                })}
              </div>
              <span className="text-xs font-mono text-slate-400 transition-all duration-500" style={{ color: stage.color }}>
                {loadingStep || stage.label}
              </span>
            </div>
            {/* Progress dots */}
            <div className="flex justify-center gap-1.5 mt-3">
              {SCAN_STAGES.map((_, i) => (
                <div
                  key={i}
                  className="rounded-full transition-all duration-500"
                  style={{
                    width: i === stageIdx ? '20px' : '6px',
                    height: '4px',
                    background: i === stageIdx ? stage.color : 'rgba(255,255,255,0.12)',
                  }}
                />
              ))}
            </div>
          </div>
        )}

        {/* Validation error */}
        {error && (
          <div className="mt-3 flex items-center gap-2 text-xs text-rose-400 bg-rose-500/8 border border-rose-500/20 rounded-xl px-4 py-2.5 animate-fade-in">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </form>

      {/* Quick sample URLs */}
      {!isLoading && (
        <div className="mt-5 flex flex-wrap items-center justify-center gap-2 animate-fade-in">
          <span className="text-xs text-slate-600 font-mono">Test with:</span>
          {SAMPLE_URLS.map(({ label, url, color }) => (
            <button
              key={label}
              type="button"
              onClick={() => handleSample(url)}
              className={`px-3 py-1.5 rounded-lg border bg-white/[0.02] text-xs font-mono transition-all duration-200 ${color}`}
            >
              {label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
