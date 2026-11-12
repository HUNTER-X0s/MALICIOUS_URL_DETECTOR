'use client';

import React, { useState } from 'react';
import { EvidenceItem } from '@/lib/types';
import {
  ShieldAlert, Globe, Server, Network, Cpu, Info,
  ChevronDown, ChevronUp, Layers, Activity, Lock
} from 'lucide-react';

interface EvidenceListProps {
  evidence: EvidenceItem[];
  limitations: string[];
}

export function EvidenceList({ evidence, limitations }: EvidenceListProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const getLayerMeta = (layer: string, contribution: string) => {
    if (contribution === 'CRITICAL' || contribution === 'HIGH') {
      return {
        icon: <ShieldAlert className="w-4 h-4 text-rose-400" />,
        label: 'Threat Signal',
        color: '#ef4444'
      };
    }
    switch (layer) {
      case 'dns':
        return {
          icon: <Server className="w-4 h-4 text-indigo-400" />,
          label: 'DNS / Network',
          color: '#6366f1'
        };
      case 'host_domain':
      case 'lexical':
        return {
          icon: <Globe className="w-4 h-4 text-violet-400" />,
          label: 'Lexical Entropy',
          color: '#8b5cf6'
        };
      case 'threat_intel':
        return {
          icon: <Network className="w-4 h-4 text-rose-400" />,
          label: 'Threat Intelligence',
          color: '#ef4444'
        };
      case 'ml':
        return {
          icon: <Activity className="w-4 h-4 text-emerald-400" />,
          label: 'ML Inference',
          color: '#10b981'
        };
      default:
        return {
          icon: <Cpu className="w-4 h-4 text-slate-400" />,
          label: 'Inspection Vector',
          color: '#94a3b8'
        };
    }
  };

  const getContributionBadge = (contrib: string) => {
    switch (contrib) {
      case 'CRITICAL':
        return 'badge-red';
      case 'HIGH':
        return 'badge-red';
      case 'MEDIUM':
        return 'badge-amber';
      case 'LOW':
        return 'badge-slate';
      default:
        return 'badge-indigo';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            <h3 className="text-xs font-mono font-bold uppercase tracking-widest text-slate-400">
              Correlated Evidence Signals ({evidence.length})
            </h3>
          </div>
          <span className="text-[11px] font-mono text-slate-600">
            Immutable Triage Chain
          </span>
        </div>

        {evidence.length === 0 ? (
          <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] text-slate-400 text-sm flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center flex-shrink-0">
              <Lock className="w-4 h-4 text-emerald-400" />
            </div>
            <div>
              <p className="text-white text-xs font-medium">No anomalous indicators identified</p>
              <p className="text-slate-500 text-[11px] mt-0.5">
                All lexical entropy models, threat intel feeds, and SSRF security invariants evaluated benign.
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-2.5">
            {evidence.map((item) => {
              const isExpanded = expandedId === item.id;
              const meta = getLayerMeta(item.layer, item.contribution);

              return (
                <div
                  key={item.id}
                  className="rounded-2xl transition-all duration-200 overflow-hidden"
                  style={{
                    background: isExpanded ? 'rgba(15, 20, 30, 0.85)' : 'rgba(15, 17, 23, 0.55)',
                    border: isExpanded ? '1px solid rgba(99, 102, 241, 0.25)' : '1px solid rgba(255, 255, 255, 0.06)',
                  }}
                >
                  <button
                    type="button"
                    onClick={() => setExpandedId(isExpanded ? null : item.id)}
                    className="w-full text-left p-4 flex items-start justify-between gap-4 select-none group"
                  >
                    <div className="flex items-start gap-3.5 min-w-0">
                      <div
                        className="mt-0.5 p-2 rounded-xl flex-shrink-0 transition-transform duration-200 group-hover:scale-105"
                        style={{
                          background: `${meta.color}15`,
                          border: `1px solid ${meta.color}30`
                        }}
                      >
                        {meta.icon}
                      </div>
                      <div className="min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-semibold text-white text-sm tracking-tight group-hover:text-indigo-200 transition-colors">
                            {item.description}
                          </span>
                          <span className={`badge ${getContributionBadge(item.contribution)}`}>
                            {item.contribution}
                          </span>
                        </div>
                        <div className="mt-1 flex items-center gap-3 text-[11px] text-slate-500 font-mono">
                          <span className="text-slate-400">Layer: {meta.label}</span>
                          <span>•</span>
                          <span>Source: {item.source}</span>
                          <span>•</span>
                          <span>Freshness: {item.freshness}</span>
                        </div>
                      </div>
                    </div>

                    <div className="text-slate-500 group-hover:text-slate-300 transition-colors p-1 flex-shrink-0">
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </div>
                  </button>

                  {isExpanded && item.technical_details && (
                    <div className="px-4 pb-4 pt-2 border-t border-white/[0.06] bg-black/40 text-xs font-mono animate-fade-in">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-[10px] text-indigo-400 uppercase tracking-widest font-bold">
                          Technical Telemetry Vector
                        </span>
                        <span className="text-[10px] text-slate-600">ID: {item.id}</span>
                      </div>
                      <pre className="p-3 rounded-xl bg-slate-950/80 border border-white/[0.05] text-slate-300 overflow-x-auto text-[11px] leading-relaxed">
                        {JSON.stringify(item.technical_details, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Transparent Scope Limitations & Blind Spots */}
      {limitations.length > 0 && (
        <div className="p-4 rounded-2xl bg-amber-500/[0.04] border border-amber-500/15">
          <div className="flex items-center gap-2 mb-2 text-xs font-mono text-amber-400/90 font-bold uppercase tracking-wider">
            <Info className="w-3.5 h-3.5" />
            <span>Honest Evaluation Disclosures & Limitations</span>
          </div>
          <ul className="space-y-1.5 text-xs text-slate-400 leading-relaxed font-mono">
            {limitations.map((lim, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-amber-500 font-bold">•</span>
                <span>{lim}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
