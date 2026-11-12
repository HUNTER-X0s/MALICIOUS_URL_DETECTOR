import React from 'react';
import { Lock, Shield, CheckCircle, Database } from 'lucide-react';

export default function PrivacyPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="mb-12">
        <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-bold px-2.5 py-1 rounded bg-emerald-500/10 border border-emerald-500/20">
          Privacy Policy & Data Governance
        </span>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight mt-4 mb-4">
          Privacy by Design & Data Minimization
        </h1>
        <p className="text-slate-400 text-base leading-relaxed">
          How URLSentinel handles inspected URLs, query parameters, network telemetry, and user privacy rights.
        </p>
      </div>

      <div className="space-y-10 text-slate-300 text-sm leading-relaxed">
        <section className="p-6 rounded-2xl glass-panel">
          <h2 className="text-lg font-bold text-white mb-3">1. Information We Collect During Scans</h2>
          <p className="mb-3">
            When you submit a URL for analysis or when the URLSentinel browser extension monitors navigation:
          </p>
          <ul className="list-disc list-inside space-y-1 text-slate-400 font-mono text-xs">
            <li>The destination hostname and path structure (for lexical and threat classification)</li>
            <li>A SHA-256 cryptographic hash of the normalized URL (for cache deduplication)</li>
            <li>Standard transport metadata (timestamp, HTTP status code of the query)</li>
          </ul>
        </section>

        <section className="p-6 rounded-2xl glass-panel">
          <h2 className="text-lg font-bold text-white mb-3">2. What We Explicitly Never Store or Collect</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-400 font-mono text-xs">
            <li>We do NOT collect user browsing history across the web.</li>
            <li>We do NOT store user credentials or passwords submitted in URLs.</li>
            <li>We do NOT store sensitive URL query tokens (OAuth tokens, API keys, session IDs are stripped).</li>
            <li>We do NOT sell or broker URL lookup data to advertising or tracking networks.</li>
          </ul>
        </section>

        <section className="p-6 rounded-2xl glass-panel">
          <h2 className="text-lg font-bold text-white mb-3">3. Browser Extension Data Access</h2>
          <p className="mb-3">
            The URLSentinel browser extension runs locally within your browser. It uses local storage caching so that
            frequently visited destinations are evaluated without making outbound network queries. Only the candidate domain
            is evaluated when navigating to unknown origins.
          </p>
        </section>

        <section className="p-6 rounded-2xl glass-panel">
          <h2 className="text-lg font-bold text-white mb-3">4. Compliance with DPDPA & GDPR</h2>
          <p>
            URLSentinel conforms to data minimization, purpose limitation, and storage limitation under the Digital Personal Data
            Protection Act (DPDPA 2023) and General Data Protection Regulation (GDPR). Any user may request the eviction of cached
            hashes by contacting privacy@urlsentinel.local.
          </p>
        </section>
      </div>
    </div>
  );
}

