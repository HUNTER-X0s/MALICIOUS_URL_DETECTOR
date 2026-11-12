import React from 'react';
import { Shield, Lock, AlertTriangle, FileCode, CheckCircle, Terminal } from 'lucide-react';

export default function SecurityPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="mb-12">
        <span className="text-xs font-mono uppercase tracking-widest text-indigo-400 font-bold px-2.5 py-1 rounded bg-indigo-500/10 border border-indigo-500/20">
          Transparency Center
        </span>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight mt-4 mb-4">
          Security Architecture & Detection Philosophy
        </h1>
        <p className="text-slate-400 text-base leading-relaxed">
          Trust in cybersecurity is earned through rigorous controls, provable isolation boundaries, and radical honesty about limitations.
        </p>
      </div>

      <div className="space-y-12">
        {/* Principle 1 */}
        <section className="p-8 rounded-3xl glass-panel border border-white/5">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400">
              <Lock className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold text-white">1. Server-Side Request Forgery (SSRF) Prevention</h2>
          </div>
          <p className="text-slate-300 text-sm leading-relaxed mb-4">
            Public link scanners are historically abused by threat actors as proxies to probe cloud metadata, internal Kubernetes clusters,
            or enterprise subnets. URLSentinel implements a strict, multi-stage destination boundary:
          </p>
          <ul className="list-disc list-inside space-y-2 text-sm text-slate-400 font-mono mb-4">
            <li>Blocks 100% of IPv4 RFC 1918 private subnets (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)</li>
            <li>Denies cloud instance metadata endpoints (169.254.169.254, 100.100.100.200)</li>
            <li>Blocks IPv6 loopback (::1), ULA (fc00::/7), and IPv4-mapped representations (::ffff:0:0/96)</li>
            <li>Detects integer, octal (0177.0.0.1), and hex (0x7f000001) numeric bypass attempts</li>
            <li>Restricts network destinations strictly to standard web ports: 80, 443, 8080, 8443</li>
          </ul>
        </section>

        {/* Principle 2 */}
        <section className="p-8 rounded-3xl glass-panel border border-white/5">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold text-white">2. The Detection Honesty Invariant (HTTPS ≠ Safe)</h2>
          </div>
          <p className="text-slate-300 text-sm leading-relaxed mb-3">
            Over 85% of modern phishing websites utilize valid TLS/SSL certificates issued via automated certificate authorities.
            URLSentinel enforces an uncompromised product invariant:
          </p>
          <div className="p-4 rounded-xl bg-slate-950 border border-white/5 font-mono text-xs text-amber-300/90 leading-relaxed">
            The presence of an HTTPS padlock merely validates connection encryption in transit; it does not attest to destination legitimacy,
            beneficial intent, or immunity from credential harvesting.
          </div>
          <p className="text-slate-300 text-sm leading-relaxed mt-3">
            Furthermore, when an external threat intelligence provider experiences an outage, URLSentinel renders an explicit <span className="font-mono text-slate-300 font-bold">UNKNOWN</span> verdict
            rather than deceptively defaulting to &ldquo;Clean&rdquo;.
          </p>
        </section>

        {/* Principle 3 */}
        <section className="p-8 rounded-3xl glass-panel border border-white/5">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400">
              <CheckCircle className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold text-white">3. Zero-Retention Privacy Architecture</h2>
          </div>
          <p className="text-slate-300 text-sm leading-relaxed mb-4">
            URLs frequently carry confidential context, including password reset tokens, OAuth bearer codes, customer account IDs,
            and private identifiers.
          </p>
          <ul className="list-disc list-inside space-y-2 text-sm text-slate-400 font-mono">
            <li>User credentials in URL authorities (user:password@host) are completely purged during parsing.</li>
            <li>Sensitive query parameters (token, session, key, auth) are automatically masked to [REDACTED].</li>
            <li>No full submitted URLs are persisted in plaintext logs or shared with third-party tracking services.</li>
          </ul>
        </section>

        {/* Principle 4 */}
        <section className="p-8 rounded-3xl glass-panel border border-white/5">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-xl bg-violet-500/10 text-violet-400">
              <Terminal className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold text-white">4. Coordinated Vulnerability Disclosure</h2>
          </div>
          <p className="text-slate-300 text-sm leading-relaxed">
            We welcome constructive reports from security researchers. If you identify an issue affecting our infrastructure,
            SSRF boundaries, or detection mechanisms, please submit an advisory directly to: <span className="font-mono text-indigo-400">security@urlsentinel.local</span>.
          </p>
        </section>
      </div>
    </div>
  );
}

