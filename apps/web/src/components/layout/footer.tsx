import React from 'react';
import Link from 'next/link';
import { Shield, Lock, FileText, CheckCircle2, Terminal, ExternalLink, Github, Heart } from 'lucide-react';

export function Footer() {
  return (
    <footer className="w-full border-t border-white/[0.06] bg-[#030712] py-16 text-slate-400 text-base relative overflow-hidden">
      {/* Subtle top glow line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-indigo-500/20 to-transparent" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-10 mb-12">
          {/* Brand Info */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-glow-sm">
                <Shield className="w-4 h-4 text-white" strokeWidth={2.5} />
              </div>
              <span className="font-bold text-white text-lg tracking-tight">URLSentinel</span>
            </div>
            <p className="text-slate-400 text-sm sm:text-base leading-relaxed max-w-sm">
              The high-assurance malicious URL detection platform. Engineered with SSRF isolation,
              lexical entropy modeling, threat feed provenance, and zero user-link retention.
            </p>
            <div className="flex flex-col gap-2 pt-2">
              <div className="flex items-center gap-2 text-sm text-emerald-400 font-mono">
                <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                <span>Zero User URL Logging / Strict Ephemeral RAM Analysis</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-indigo-400 font-mono">
                <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                <span>Cryptographically Signed RFC 7515 Verdict Receipts</span>
              </div>
            </div>
          </div>

          {/* Defense Architecture */}
          <div>
            <h4 className="text-sm font-mono font-bold text-white uppercase tracking-wider mb-4">
              Architecture
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link href="/security#ssrf" className="hover:text-white transition-colors flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
                  SSRF Defense Boundary
                </Link>
              </li>
              <li>
                <Link href="/security#shannon" className="hover:text-white transition-colors flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-violet-500" />
                  Shannon Entropy Analysis
                </Link>
              </li>
              <li>
                <Link href="/security#homoglyphs" className="hover:text-white transition-colors flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  Homoglyph Detection
                </Link>
              </li>
              <li>
                <Link href="/security#feeds" className="hover:text-white transition-colors flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                  Threat Feed Correlation
                </Link>
              </li>
            </ul>
          </div>

          {/* Governance & Trust */}
          <div>
            <h4 className="text-sm font-mono font-bold text-white uppercase tracking-wider mb-4">
              Trust & Ethics
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link href="/privacy" className="hover:text-white transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/security" className="hover:text-white transition-colors">
                  Transparency Center
                </Link>
              </li>
              <li>
                <Link href="/security#honesty" className="hover:text-white transition-colors">
                  Detection Honesty Policy
                </Link>
              </li>
              <li>
                <Link href="/security#disclosure" className="hover:text-white transition-colors">
                  Responsible Disclosure
                </Link>
              </li>
            </ul>
          </div>

          {/* Developer & Integration */}
          <div>
            <h4 className="text-sm font-mono font-bold text-white uppercase tracking-wider mb-4">
              Developers
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li>
                <a
                  href="http://localhost:8000/docs"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-white transition-colors flex items-center gap-1"
                >
                  <span>OpenAPI 3.1 Specs</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a
                  href="#extension"
                  className="hover:text-white transition-colors"
                >
                  Browser Extension (MV3)
                </a>
              </li>
              <li>
                <Link href="/security#status" className="hover:text-white transition-colors">
                  System Health & SLA
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar with Invariant Guarantee */}
        <div className="pt-8 border-t border-white/[0.06] flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-slate-500">
          <p className="font-mono">
            © {new Date().getFullYear()} URLSentinel Organization. Built with Zero-Trust Security Engineering.
          </p>
          <div className="flex items-center gap-4 font-mono text-xs text-slate-400">
            <span className="px-2.5 py-1 rounded-md bg-white/[0.03] border border-white/[0.06]">
              Honesty Invariant: No system can guarantee 100% detection.
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
