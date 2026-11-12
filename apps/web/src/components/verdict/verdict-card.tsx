'use client';

import React, { useState, useEffect, useRef } from 'react';
import { VerdictResult } from '@/lib/types';
import { EvidenceList } from './evidence-list';
import {
  ShieldAlert, AlertTriangle, HelpCircle, ShieldCheck,
  Copy, Check, Terminal, ChevronDown, ChevronUp,
  ExternalLink, Flag, Hash, Info
} from 'lucide-react';

interface VerdictCardProps {
  result: VerdictResult;
}

type VerdictTheme = {
  icon: React.ReactNode;
  title: string;
  subtitle: string;
  accentColor: string;
  glowClass: string;
  borderColor: string;
  bgGlow: string;
  badgeBg: string;
  badgeText: string;
  badgeBorder: string;
  ringClass: string;
};

function getTheme(verdict: string): VerdictTheme {
  switch (verdict) {
    case 'MALICIOUS':
      return {
        icon: <ShieldAlert className="w-7 h-7" style={{ color: '#ef4444' }} />,
        title: 'Malicious Destination',
        subtitle: 'Threat signals confirmed — do not visit this URL',
        accentColor: '#ef4444',
        glowClass: 'animate-pulse-glow-danger',
        borderColor: 'rgba(239,68,68,0.3)',
        bgGlow: 'radial-gradient(ellipse 80% 50% at 50% -5%, rgba(239,68,68,0.14), transparent 70%)',
        badgeBg: 'rgba(239,68,68,0.1)',
        badgeText: '#f87171',
        badgeBorder: 'rgba(239,68,68,0.3)',
        ringClass: 'glow-ring-danger',
      };
    case 'SUSPICIOUS':
      return {
        icon: <AlertTriangle className="w-7 h-7" style={{ color: '#f59e0b' }} />,
        title: 'Suspicious Indicators',
        subtitle: 'Multiple anomalies detected — proceed with extreme caution',
        accentColor: '#f59e0b',
        glowClass: 'animate-pulse-glow-warn',
        borderColor: 'rgba(245,158,11,0.3)',
        bgGlow: 'radial-gradient(ellipse 80% 50% at 50% -5%, rgba(245,158,11,0.12), transparent 70%)',
        badgeBg: 'rgba(245,158,11,0.1)',
        badgeText: '#fbbf24',
        badgeBorder: 'rgba(245,158,11,0.3)',
        ringClass: 'glow-ring-warn',
      };
    case 'BENIGN':
      return {
        icon: <ShieldCheck className="w-7 h-7" style={{ color: '#10b981' }} />,
        title: 'No Threats Detected',
        subtitle: 'Destination appears safe based on current intelligence',
        accentColor: '#10b981',
        glowClass: 'animate-pulse-glow-safe',
        borderColor: 'rgba(16,185,129,0.3)',
        bgGlow: 'radial-gradient(ellipse 80% 50% at 50% -5%, rgba(16,185,129,0.1), transparent 70%)',
        badgeBg: 'rgba(16,185,129,0.1)',
        badgeText: '#34d399',
        badgeBorder: 'rgba(16,185,129,0.3)',
        ringClass: 'glow-ring-safe',
      };
    default: // UNKNOWN
      return {
        icon: <HelpCircle className="w-7 h-7" style={{ color: '#94a3b8' }} />,
        title: 'Inconclusive Result',
        subtitle: 'Insufficient signals — unknown or inaccessible destination',
        accentColor: '#94a3b8',
        glowClass: '',
        borderColor: 'rgba(100,116,139,0.25)',
        bgGlow: 'radial-gradient(ellipse 80% 50% at 50% -5%, rgba(100,116,139,0.08), transparent 70%)',
        badgeBg: 'rgba(100,116,139,0.1)',
        badgeText: '#94a3b8',
        badgeBorder: 'rgba(100,116,139,0.2)',
        ringClass: '',
      };
  }
}

/** Animated circular arc gauge for risk score */
function RiskGauge({ score, accentColor }: { score: number; accentColor: string }) {
  const [animScore, setAnimScore] = useState(0);
  const radius = 46;
  const circumference = 2 * Math.PI * radius;
  // Arc fills from 220° to -40° (280° total sweep)
  const sweep = 280;
  const offset = circumference - (animScore / 100) * (circumference * sweep / 360);

  useEffect(() => {
    const start = Date.now();
    const duration = 1000;
    const raf = () => {
      const elapsed = Date.now() - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setAnimScore(Math.round(score * eased));
      if (progress < 1) requestAnimationFrame(raf);
    };
    requestAnimationFrame(raf);
  }, [score]);

  const scoreLabel =
    score >= 75 ? 'Critical Risk' :
    score >= 50 ? 'High Risk' :
    score >= 25 ? 'Moderate Risk' : 'Low Risk';

  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative w-28 h-28">
        <svg className="w-full h-full -rotate-[130deg]" viewBox="0 0 112 112">
          {/* Track */}
          <circle
            cx="56" cy="56" r={radius}
            fill="none"
            stroke="rgba(255,255,255,0.05)"
            strokeWidth="8"
            strokeDasharray={`${circumference * sweep / 360} ${circumference}`}
            strokeLinecap="round"
          />
          {/* Filled arc */}
          <circle
            cx="56" cy="56" r={radius}
            fill="none"
            stroke={accentColor}
            strokeWidth="8"
            strokeDasharray={`${circumference * sweep / 360} ${circumference}`}
            strokeDashoffset={offset}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 0.05s linear', filter: `drop-shadow(0 0 6px ${accentColor}66)` }}
          />
        </svg>
        {/* Center score */}
        <div className="absolute inset-0 flex flex-col items-center justify-center mt-2">
          <span className="text-2xl font-black text-white font-mono" style={{ color: accentColor }}>
            {animScore}
          </span>
          <span className="text-[9px] text-slate-500 font-mono uppercase tracking-wider">/ 100</span>
        </div>
      </div>
      <div className="text-xs font-semibold" style={{ color: accentColor }}>{scoreLabel}</div>
      <div className="text-[10px] text-slate-500 font-mono">Risk Score</div>
    </div>
  );
}

export function VerdictCard({ result }: VerdictCardProps) {
  const [copied, setCopied] = useState(false);
  const [showTechnical, setShowTechnical] = useState(false);
  const [mounted, setMounted] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

  const theme = getTheme(result.verdict);

  useEffect(() => {
    // Trigger mount animation
    const t = setTimeout(() => setMounted(true), 50);
    return () => clearTimeout(t);
  }, []);

  const handleCopyUrl = () => {
    navigator.clipboard.writeText(result.url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const confidenceColor =
    result.confidence === 'HIGH' ? '#10b981' :
    result.confidence === 'MEDIUM' ? '#f59e0b' : '#94a3b8';

  return (
    <div
      ref={cardRef}
      className="w-full max-w-4xl mx-auto rounded-3xl overflow-hidden relative"
      style={{
        opacity: mounted ? 1 : 0,
        transform: mounted ? 'translateY(0) scale(1)' : 'translateY(20px) scale(0.98)',
        transition: 'opacity 0.5s ease, transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)',
        background: 'rgba(10, 13, 20, 0.85)',
        backdropFilter: 'blur(32px)',
        border: `1px solid ${theme.borderColor}`,
        boxShadow: `0 24px 80px rgba(0,0,0,0.6), 0 0 0 1px ${theme.borderColor}, 0 0 60px ${theme.accentColor}18`,
      }}
    >
      {/* Background glow */}
      <div className="absolute inset-0 pointer-events-none" style={{ background: theme.bgGlow }} />

      {/* Top accent stripe */}
      <div
        className="h-1 w-full"
        style={{ background: `linear-gradient(90deg, transparent, ${theme.accentColor}, transparent)`, opacity: 0.6 }}
      />

      <div className="relative p-6 sm:p-8">

        {/* ── Header Row ─────────────────────────────────────── */}
        <div className="flex flex-col sm:flex-row gap-6 pb-6 border-b" style={{ borderColor: 'rgba(255,255,255,0.07)' }}>

          {/* Left: verdict icon + labels */}
          <div className="flex items-start gap-4 flex-1 min-w-0">
            {/* Animated icon bubble */}
            <div
              className={`flex-shrink-0 w-14 h-14 rounded-2xl flex items-center justify-center ${theme.glowClass}`}
              style={{
                background: `${theme.accentColor}18`,
                border: `1px solid ${theme.accentColor}40`,
              }}
            >
              {theme.icon}
            </div>

            <div className="min-w-0 pt-0.5">
              {/* Verdict badge + timestamp */}
              <div className="flex items-center flex-wrap gap-2 mb-2">
                <span
                  className="text-[10px] font-mono font-bold px-2.5 py-1 rounded-lg uppercase tracking-widest"
                  style={{
                    background: theme.badgeBg,
                    color: theme.badgeText,
                    border: `1px solid ${theme.badgeBorder}`,
                  }}
                >
                  ● {result.verdict}
                </span>
                <span className="text-[10px] text-slate-600 font-mono">
                  {new Date(result.checked_at).toLocaleString()}
                </span>
              </div>
              <h2 className="text-xl sm:text-2xl font-extrabold text-white leading-tight">{theme.title}</h2>
              <p className="text-sm text-slate-400 mt-1 leading-snug">{theme.subtitle}</p>
            </div>
          </div>

          {/* Right: risk gauge */}
          <div className="flex-shrink-0 flex items-center justify-center sm:justify-end">
            <RiskGauge score={result.risk_score} accentColor={theme.accentColor} />
          </div>
        </div>

        {/* ── Destination URL bar ─────────────────────────────── */}
        <div
          className="mt-5 flex items-center justify-between gap-3 px-4 py-3 rounded-xl font-mono text-xs"
          style={{ background: 'rgba(5,7,12,0.7)', border: '1px solid rgba(255,255,255,0.05)' }}
        >
          <div className="flex items-center gap-2 min-w-0 flex-1">
            <Hash className="w-3.5 h-3.5 text-slate-600 flex-shrink-0" />
            <span className="text-slate-300 truncate select-all">{result.url}</span>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <span className="hidden sm:inline text-slate-600 text-[10px]">{result.url_hash.slice(0, 10)}…</span>
            <button
              onClick={handleCopyUrl}
              className="p-1.5 rounded-lg hover:bg-white/[0.07] text-slate-400 hover:text-white transition-colors"
              title="Copy URL"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
          </div>
        </div>

        {/* ── Recommended Action ──────────────────────────────── */}
        <div
          className="mt-5 p-4 rounded-2xl"
          style={{
            background: `${theme.accentColor}0D`,
            border: `1px solid ${theme.accentColor}30`,
          }}
        >
          <div
            className="text-[10px] font-mono font-bold uppercase tracking-widest mb-1"
            style={{ color: theme.accentColor }}
          >
            Recommended Action
          </div>
          <p className="text-sm text-slate-200 font-medium leading-relaxed">{result.recommended_action}</p>
        </div>

        {/* ── Summary ─────────────────────────────────────────── */}
        <p className="mt-5 text-sm text-slate-300 leading-relaxed">{result.summary}</p>

        {/* ── Confidence + metadata row ────────────────────────── */}
        <div className="mt-5 flex flex-wrap gap-3">
          {/* Confidence */}
          <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white/[0.03] border border-white/[0.06] text-xs">
            <span className="text-slate-500 font-mono">Confidence</span>
            <span className="font-bold font-mono" style={{ color: confidenceColor }}>{result.confidence}</span>
          </div>
          {/* Contract version */}
          <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white/[0.03] border border-white/[0.06] text-xs font-mono text-slate-500">
            Schema: {result.contract_version}
          </div>
          {/* Limitations warning */}
          {result.limitations.length > 0 && (
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-amber-500/5 border border-amber-500/15 text-xs text-amber-500/80 font-mono">
              <Info className="w-3 h-3" />
              {result.limitations.length} limitation{result.limitations.length > 1 ? 's' : ''} noted
            </div>
          )}
        </div>

        {/* ── Evidence ─────────────────────────────────────────── */}
        <div className="mt-8">
          <EvidenceList evidence={result.evidence} limitations={result.limitations} />
        </div>

        {/* ── Technical Details Toggle ─────────────────────────── */}
        <div className="mt-8 pt-6" style={{ borderTop: '1px solid rgba(255,255,255,0.07)' }}>
          <button
            type="button"
            onClick={() => setShowTechnical(!showTechnical)}
            className="flex items-center gap-2 text-xs font-mono text-slate-500 hover:text-slate-200 transition-colors group w-full"
          >
            <Terminal className="w-4 h-4 text-indigo-500 group-hover:text-indigo-400 transition-colors" />
            <span>Technical Parameters</span>
            {showTechnical
              ? <ChevronUp className="w-3.5 h-3.5 ml-auto" />
              : <ChevronDown className="w-3.5 h-3.5 ml-auto" />}
          </button>

          {showTechnical && (
            <div className="mt-4 animate-fade-in-up">
              <div className="terminal">
                <div className="terminal-header">
                  <div className="terminal-dot" style={{ background: '#ef4444' }} />
                  <div className="terminal-dot" style={{ background: '#f59e0b' }} />
                  <div className="terminal-dot" style={{ background: '#10b981' }} />
                  <span className="ml-2 text-slate-500 text-[10px] font-mono">urlsentinel://technical-parameters</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-6 gap-y-3 text-xs">
                  {[
                    ['scheme',         result.technical_details.scheme],
                    ['host',           result.technical_details.host],
                    ['path',           result.technical_details.path || '/'],
                    ['port',           result.technical_details.port ?? 'default'],
                    ['entropy',        result.technical_details.entropy.toFixed(4)],
                    ['query_params',   result.technical_details.query_params_count],
                    ['ip_host',        result.technical_details.is_ip_host ? 'TRUE ⚠' : 'false'],
                    ['url_shortener',  result.technical_details.is_shortener ? 'TRUE ⚠' : 'false'],
                    ['punycode',       result.technical_details.punycode ?? 'none'],
                  ].map(([k, v]) => (
                    <div key={String(k)}>
                      <span className="text-indigo-500">{k}</span>
                      <span className="text-slate-500"> = </span>
                      <span className="text-emerald-400 break-all">{String(v)}</span>
                    </div>
                  ))}
                </div>

                {result.technical_details.suspicious_tokens.length > 0 && (
                  <div className="mt-4 pt-4" style={{ borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                    <span className="text-indigo-500">suspicious_tokens</span>
                    <span className="text-slate-500"> = [</span>
                    <span className="text-rose-400">
                      {result.technical_details.suspicious_tokens.map(t => `"${t}"`).join(', ')}
                    </span>
                    <span className="text-slate-500">]</span>
                  </div>
                )}

                {result.technical_details.typosquatting_matches.length > 0 && (
                  <div className="mt-2">
                    <span className="text-indigo-500">typosquatting_matches</span>
                    <span className="text-slate-500"> = [</span>
                    <span className="text-rose-400">
                      {result.technical_details.typosquatting_matches.map(t => `"${t}"`).join(', ')}
                    </span>
                    <span className="text-slate-500">]</span>
                  </div>
                )}

                {result.technical_details.resolved_ips && result.technical_details.resolved_ips.length > 0 && (
                  <div className="mt-2">
                    <span className="text-indigo-500">resolved_ips</span>
                    <span className="text-slate-500"> = [</span>
                    <span className="text-amber-400">
                      {result.technical_details.resolved_ips.map(ip => `"${ip}"`).join(', ')}
                    </span>
                    <span className="text-slate-500">]</span>
                  </div>
                )}

                <div className="mt-4 pt-3" style={{ borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                  <span className="text-slate-600 text-[10px]">
                    scan_id: {result.id} · expires: {new Date(result.expires_at).toLocaleString()}
                  </span>
                </div>
              </div>

              {/* False positive reporting link */}
              <div className="mt-3 flex items-center gap-2 text-xs text-slate-600">
                <Flag className="w-3 h-3" />
                <span>Incorrect verdict?</span>
                <a
                  href={`/report?id=${result.id}`}
                  className="text-indigo-400 hover:text-indigo-300 transition-colors underline underline-offset-2"
                >
                  Report a false positive
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
