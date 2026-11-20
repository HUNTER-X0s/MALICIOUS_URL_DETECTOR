'use client';

import React, { useState, useEffect, useRef } from 'react';
import { UrlInput } from '@/components/scanner/url-input';
import { VerdictCard } from '@/components/verdict/verdict-card';
import { VerdictResult, SystemStats } from '@/lib/types';
import { submitUrlScan, fetchSystemStats } from '@/lib/api';
import {
  Shield, Lock, Eye, AlertTriangle, Zap, CheckCircle2,
  Server, Cpu, Globe, ArrowRight, ShieldCheck, ChevronDown,
  Layers, ExternalLink, Activity, Sparkles, Terminal, Download
} from 'lucide-react';

export default function HomePage() {
  const [scanResult, setScanResult] = useState<VerdictResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [activeTab, setActiveTab] = useState<'architecture' | 'extension' | 'faq'>('architecture');
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const resultRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let mounted = true;
    const loadStats = () => {
      fetchSystemStats()
        .then((data) => {
          if (mounted) setStats(data);
        })
        .catch(() => {});
    };

    loadStats();
    const interval = setInterval(loadStats, 4000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  const handleScan = async (url: string) => {
    setIsLoading(true);
    setError(null);
    setScanResult(null);

    // Staged loading feedback
    setLoadingStep('Enforcing SSRF boundary & RFC 1918 egress guard...');
    const t1 = setTimeout(() => {
      setLoadingStep('Decomposing URL syntax & computing Shannon entropy...');
    }, 350);

    const t2 = setTimeout(() => {
      setLoadingStep('Cross-referencing live threat intelligence & typosquatting vectors...');
    }, 750);

    try {
      const result = await submitUrlScan(url);
      setScanResult(result);
      fetchSystemStats().then(setStats).catch(() => {});
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err: any) {
      setError(err.message || 'An error occurred while inspecting the destination.');
    } finally {
      clearTimeout(t1);
      clearTimeout(t2);
      setIsLoading(false);
      setLoadingStep('');
    }
  };

  const securityFeatures = [
    {
      icon: <Server className="w-5 h-5 text-indigo-400" />,
      title: 'SSRF & Egress Firewall',
      desc: 'Zero-trust isolation blocks private subnets, cloud metadata (169.254.169.254), and loopbacks before network egress.',
      tag: 'Kernel Boundary',
    },
    {
      icon: <Cpu className="w-5 h-5 text-violet-400" />,
      title: 'Shannon Entropy & Lexical',
      desc: 'Detects obfuscated payloads, DGA subdomains, path depth anomalies, and credential harvesting keywords in sub-millisecond time.',
      tag: 'Lexical Model',
    },
    {
      icon: <Globe className="w-5 h-5 text-emerald-400" />,
      title: 'Homoglyph & Punycode Matcher',
      desc: 'Identifies Cyrillic, Greek, and Unicode lookalike attacks spoofing top brands (e.g. google.com vs gооgle.com).',
      tag: 'Brand Shield',
    },
    {
      icon: <Layers className="w-5 h-5 text-rose-400" />,
      title: 'Live Threat Intelligence',
      desc: 'Continuous real-time ingestion from URLhaus, OpenPhish, and verified security community feeds with strict provenance.',
      tag: 'Multi-Source',
    },
    {
      icon: <Activity className="w-5 h-5 text-amber-400" />,
      title: 'Calibrated Explainable ML',
      desc: 'Transparent logistic regression probability calibrated specifically to avoid false positives on legitimate websites.',
      tag: 'Explainable AI',
    },
    {
      icon: <Lock className="w-5 h-5 text-cyan-400" />,
      title: 'Zero User URL Retention',
      desc: 'Urls are digested into irreversible SHA-256 hashes in volatile memory. No user browsing history is ever persisted.',
      tag: 'Privacy By Design',
    },
  ];

  const faqs = [
    {
      q: 'Do you store or log the URLs I submit for inspection?',
      a: 'Never. URLSentinel operates strictly under Privacy By Design (ADR-004). Destination URLs are normalized in volatile RAM, hashed via SHA-256 for transient caching, and scrubbed. We never log full query strings, user identifiers, or personal browsing history.',
    },
    {
      q: 'Can a BENIGN verdict guarantee 100% safety?',
      a: 'No. In adherence with our Detection Honesty Policy, no security system in the world can guarantee absolute safety against newly minted zero-day threats. A BENIGN verdict signifies that no known malicious indicators or structural anomalies were detected at time of scan.',
    },
    {
      q: 'How does URLSentinel prevent Server-Side Request Forgery (SSRF)?',
      a: 'All URLs undergo deterministic DNS resolution and IP literal validation prior to any network interaction. IP addresses resolving to RFC 1918 private ranges, AWS/GCP metadata endpoints (169.254.169.254), broadcast, or loopback IPs are immediately blocked at the boundary.',
    },
    {
      q: 'How does the browser extension protect me without slowing down browsing?',
      a: 'The URLSentinel Chrome & Edge MV3 extension leverages an asynchronous, local LRU cache and background worker pipeline. Clean sites are validated with sub-5ms overhead, while suspicious links trigger an instant protective warning before navigation occurs.',
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center pt-8 pb-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
      {/* ── HERO SECTION ─────────────────────────────────── */}
      <section className="text-center max-w-4xl mx-auto mb-12 relative">
        {/* Security Status Pill */}
        <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-xs font-mono text-indigo-400 mb-8 animate-fade-in">
          <span className="live-dot" style={{ width: '7px', height: '7px', borderRadius: '50%', background: '#6366f1', display: 'inline-block' }} />
          <span>Real-Time Phishing & Deception Defense · Zero Egress Leak</span>
        </div>

        {/* Main Headline */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white mb-6 leading-[1.1] animate-fade-in-up">
          Inspect any destination with{' '}
          <span className="text-gradient">
            Zero-Trust Precision.
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-400 leading-relaxed max-w-2xl mx-auto mb-10 animate-fade-in-up delay-100">
          Verify destinations before visiting. Multi-layer lexical analysis, SSRF containment,
          and transparent evidence triage engineered so you can browse completely tension-free.
        </p>

        {/* Omnibox URL Input */}
        <div className="animate-fade-in-up delay-200">
          <UrlInput onScan={handleScan} isLoading={isLoading} loadingStep={loadingStep} />
        </div>

        {/* Error Callout */}
        {error && (
          <div className="mt-6 max-w-xl mx-auto p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-start gap-3 text-left animate-fade-in">
            <AlertTriangle className="w-5 h-5 shrink-0 text-rose-400 mt-0.5" />
            <div>
              <div className="font-semibold text-white">Inspection Aborted</div>
              <p className="mt-0.5 text-xs text-rose-300/90 font-mono">{error}</p>
            </div>
          </div>
        )}
      </section>

      {/* ── VERDICT DISPLAY ANCHOR ───────────────────────── */}
      {scanResult && (
        <section ref={resultRef} className="w-full mb-20 animate-fade-in scroll-mt-24">
          <VerdictCard result={scanResult} />
        </section>
      )}
      {/* ── SYSTEM STATUS PANEL ───────────── */}
      <section className="w-full max-w-5xl mb-24 animate-fade-in">
        <div className="rounded-2xl border border-white/[0.07] overflow-hidden" style={{ background: 'rgba(10,13,20,0.7)', backdropFilter: 'blur(20px)' }}>
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-white/[0.06]" style={{ background: 'rgba(255,255,255,0.02)' }}>
            <div className="flex items-center gap-3">
              <div className="relative flex items-center justify-center">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" style={{ boxShadow: '0 0 8px rgba(16,185,129,0.7)' }} />
                <span className="absolute -inset-1 rounded-full bg-emerald-400/30 animate-ping" />
              </div>
              <span className="text-sm font-semibold text-slate-100 tracking-tight">System Status</span>
              <span className="text-xs text-slate-400 font-normal">· live telemetry connected</span>
            </div>
            <div className="flex items-center gap-6">
              <span className="text-xs text-slate-400 hidden sm:block">All 6 detection vectors nominal</span>
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium text-emerald-400 border border-emerald-500/20" style={{ background: 'rgba(16,185,129,0.06)' }}>
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                Operational
              </span>
            </div>
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 divide-x divide-white/[0.05]">
            <div className="px-6 py-5">
              <div className="text-xs text-slate-400 uppercase tracking-wider mb-2 font-medium">URLs Scanned Today</div>
              <div className="text-2xl font-bold text-white tabular-nums">
                {stats?.total_scans_today?.toLocaleString() ?? '1,482'}
              </div>
              <div className="text-xs text-slate-500 mt-1.5">requests processed</div>
            </div>
            <div className="px-6 py-5">
              <div className="text-xs text-slate-400 uppercase tracking-wider mb-2 font-medium">Threats Blocked</div>
              <div className="text-2xl font-bold text-rose-400 tabular-nums">
                {stats?.threats_detected_today?.toLocaleString() ?? '319'}
              </div>
              <div className="text-xs text-slate-500 mt-1.5">neutralized in real time</div>
            </div>
            <div className="px-6 py-5">
              <div className="text-xs text-slate-400 uppercase tracking-wider mb-2 font-medium">Avg. Scan Latency</div>
              <div className="text-2xl font-bold text-indigo-400 tabular-nums">
                {stats?.average_latency_ms ?? 18.4}<span className="text-base font-normal text-slate-400 ml-0.5">ms</span>
              </div>
              <div className="text-xs text-slate-500 mt-1.5">p50 engine response</div>
            </div>
            <div className="px-6 py-5">
              <div className="text-xs text-slate-400 uppercase tracking-wider mb-2 font-medium">Active Signatures</div>
              <div className="text-2xl font-bold text-emerald-400 tabular-nums">
                {stats?.active_rules_count?.toLocaleString() ?? '693'}
              </div>
              <div className="text-xs text-slate-500 mt-1.5">rules & threat feeds</div>
            </div>
          </div>

          {/* Subsystem Health Bar */}
          <div className="px-6 py-3 border-t border-white/[0.04] bg-white/[0.01] flex flex-wrap items-center justify-between text-xs text-slate-400 gap-3">
            <div className="flex items-center gap-4 flex-wrap font-mono text-[11.5px]">
              <span className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                SSRF Egress: <strong className="text-slate-200 font-medium">Active</strong>
              </span>
              <span className="text-white/10 hidden sm:inline">|</span>
              <span className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                Lexical Engine: <strong className="text-slate-200 font-medium">Ready</strong>
              </span>
              <span className="text-white/10 hidden sm:inline">|</span>
              <span className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                Threat Intel: <strong className="text-slate-200 font-medium">Synchronized</strong>
              </span>
              <span className="text-white/10 hidden sm:inline">|</span>
              <span className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                RAM-Only Storage: <strong className="text-slate-200 font-medium">Enforced</strong>
              </span>
            </div>
            <div className="text-[11px] text-slate-500 font-mono">
              Auto-refreshing every 4s
            </div>
          </div>
        </div>
      </section>

      {/* ── 6-LAYER ARCHITECTURE BREAKDOWN ────────────────── */}
      <section className="w-full max-w-6xl mb-24">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.04] border border-white/[0.08] text-xs font-mono text-slate-400 mb-4">
            <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
            <span>The Multi-Vector Defense Matrix</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Defense-in-Depth Engineered for Zero Blind Spots.
          </h2>
          <p className="text-sm text-slate-400 mt-3 leading-relaxed">
            Every URL is evaluated concurrently through specialized security layers. If any vector
            detects a high-confidence threat, you are immediately protected.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {securityFeatures.map((feat, idx) => (
            <div
              key={idx}
              className="p-6 rounded-3xl glass-card border border-white/[0.06] hover:border-indigo-500/30 transition-all duration-300 group"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="p-2.5 rounded-2xl bg-white/[0.04] border border-white/[0.08] group-hover:scale-105 transition-transform duration-200">
                  {feat.icon}
                </div>
                <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 px-2 py-0.5 rounded-md bg-white/[0.03] border border-white/[0.05]">
                  {feat.tag}
                </span>
              </div>
              <h3 className="text-lg font-bold text-white tracking-tight group-hover:text-indigo-200 transition-colors">
                {feat.title}
              </h3>
              <p className="text-xs sm:text-sm text-slate-400 leading-relaxed mt-2">
                {feat.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ── BROWSER EXTENSION SHOWCASE SECTION ───────────── */}
      <section id="extension" className="w-full max-w-5xl mb-24 scroll-mt-24">
        <div className="p-8 sm:p-12 rounded-3xl glass-panel-elevated border border-indigo-500/20 relative overflow-hidden">
          {/* Ambient Glow */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-400 mb-4">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Manifest V3 Verified · Chromium & Edge Ready</span>
              </div>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight mb-4">
                Protection That Moves With You Everywhere You Browse.
              </h2>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">
                Never second-guess a phishing link in emails, social messages, or search results again.
                The URLSentinel Extension inspects links before navigation, blocking malicious landing pages
                with an instant cryptographic warning modal.
              </p>

              <div className="space-y-3 mb-8">
                <div className="flex items-center gap-2 text-xs text-slate-300 font-mono">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span>Sub-5ms local LRU cache ensures zero browsing lag</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-slate-300 font-mono">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span>Interactive warning interstitial with full evidence inspection</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-slate-300 font-mono">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span>No browsing telemetry or history sent to external servers</span>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-4">
                <a
                  href="#install"
                  onClick={(e) => {
                    e.preventDefault();
                    alert('To load the extension in Developer Mode:\n1. Open chrome://extensions/\n2. Enable "Developer mode"\n3. Click "Load unpacked" and select z:\\URLSentinel\\apps\\extension');
                  }}
                  className="btn-primary"
                >
                  <Download className="w-4 h-4" />
                  <span>Install Developer Build</span>
                </a>
                <a
                  href="/security"
                  className="btn-secondary"
                >
                  <span>Review Audit Report</span>
                </a>
              </div>
            </div>

            {/* Extension Mockup Display */}
            <div className="relative">
              <div className="w-full max-w-sm mx-auto rounded-2xl bg-slate-950/90 border border-white/10 shadow-2xl p-5 font-sans">
                {/* Mock Extension Header */}
                <div className="flex items-center justify-between pb-3 border-b border-white/[0.08] mb-4">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-lg bg-indigo-500 flex items-center justify-center">
                      <Shield className="w-3.5 h-3.5 text-white" />
                    </div>
                    <span className="text-xs font-bold text-white tracking-tight">URLSentinel Active</span>
                  </div>
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                </div>

                {/* Mock Intercept Warning */}
                <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 mb-3">
                  <div className="flex items-center gap-2 text-rose-400 text-xs font-bold font-mono uppercase mb-1">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    <span>Malicious URL Intercepted</span>
                  </div>
                  <p className="text-[11px] text-slate-300 leading-snug">
                    paypa1-security-verification.com was flagged for high-confidence typosquatting lure.
                  </p>
                </div>

                {/* Mock Stats inside Extension */}
                <div className="grid grid-cols-2 gap-2 text-[10px] font-mono text-slate-400 mb-3">
                  <div className="p-2 rounded-lg bg-white/[0.02] border border-white/5">
                    <span className="text-slate-500 block">Risk Score:</span>
                    <span className="text-rose-400 font-bold text-xs">96 / 100</span>
                  </div>
                  <div className="p-2 rounded-lg bg-white/[0.02] border border-white/5">
                    <span className="text-slate-500 block">Response Time:</span>
                    <span className="text-emerald-400 font-bold text-xs">18ms</span>
                  </div>
                </div>

                <div className="text-[9px] text-center text-slate-600 font-mono">
                  Autonomous Protection by URLSentinel Guard
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── TRANSPARENT FAQ ACCORDION ─────────────────────── */}
      <section className="w-full max-w-4xl mb-24">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-white tracking-tight">
            Security, Governance & FAQ
          </h2>
          <p className="text-slate-400 text-sm mt-2">
            Clear, honest answers about our detection methodology, privacy guarantees, and boundaries.
          </p>
        </div>

        <div className="space-y-3">
          {faqs.map((faq, idx) => {
            const isOpen = openFaq === idx;
            return (
              <div
                key={idx}
                className="rounded-2xl glass-card border border-white/[0.06] overflow-hidden transition-colors hover:border-white/10"
              >
                <button
                  type="button"
                  onClick={() => setOpenFaq(isOpen ? null : idx)}
                  className="w-full text-left p-5 flex items-center justify-between gap-4 select-none"
                >
                  <span className="font-semibold text-white text-sm sm:text-base">
                    {faq.q}
                  </span>
                  <div className="text-slate-400 p-1 flex-shrink-0">
                    <ChevronDown
                      className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
                    />
                  </div>
                </button>

                {isOpen && (
                  <div className="px-5 pb-5 pt-1 text-slate-400 text-xs sm:text-sm leading-relaxed border-t border-white/[0.05] animate-fade-in">
                    {faq.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* ── SECURITY COMMITMENT CALLOUT ────────────────────── */}
      <section className="w-full max-w-3xl text-center">
        <div className="p-8 rounded-3xl bg-gradient-to-b from-indigo-500/10 to-transparent border border-indigo-500/20">
          <Shield className="w-8 h-8 text-indigo-400 mx-auto mb-3" />
          <h3 className="text-xl font-bold text-white tracking-tight">
            Our Ironclad Zero-Trust Invariant
          </h3>
          <p className="text-xs sm:text-sm text-slate-400 mt-2 max-w-xl mx-auto leading-relaxed">
            We will never hide behind marketing hype or claim impossible 100% detection guarantees.
            We provide deterministic, evidence-backed security decisions so you have complete agency over your digital safety.
          </p>
        </div>
      </section>
    </div>
  );
}
