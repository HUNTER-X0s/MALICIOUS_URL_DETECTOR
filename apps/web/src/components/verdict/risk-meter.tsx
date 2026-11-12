'use client';

import React from 'react';
import { Confidence } from '@/lib/types';

interface RiskMeterProps {
  score: number;
  confidence: Confidence;
}

export function RiskMeter({ score, confidence }: RiskMeterProps) {
  // Determine severity tier and color
  let colorClass = 'from-emerald-500 to-emerald-400 text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
  let tierLabel = 'Low Threat Probability';

  if (score >= 80) {
    colorClass = 'from-rose-600 to-rose-400 text-rose-400 bg-rose-500/10 border-rose-500/20';
    tierLabel = 'Critical Danger';
  } else if (score >= 45) {
    colorClass = 'from-amber-600 to-amber-400 text-amber-400 bg-amber-500/10 border-amber-500/20';
    tierLabel = 'Suspicious Anomalies';
  } else if (score >= 25) {
    colorClass = 'from-slate-500 to-slate-400 text-slate-300 bg-slate-500/10 border-slate-500/20';
    tierLabel = 'Elevated Caution';
  }

  return (
    <div className="w-full bg-slate-900/50 border border-white/5 rounded-2xl p-5">
      <div className="flex items-center justify-between mb-3">
        <div>
          <span className="text-xs uppercase font-mono tracking-wider text-slate-400">Risk Assessment</span>
          <div className="text-xl font-bold text-white tracking-tight flex items-baseline gap-2 mt-0.5">
            <span>{score}</span>
            <span className="text-xs text-slate-400 font-mono">/ 100</span>
            <span className={`text-xs px-2 py-0.5 rounded-full border font-semibold ${colorClass}`}>
              {tierLabel}
            </span>
          </div>
        </div>

        <div className="text-right">
          <span className="text-xs uppercase font-mono tracking-wider text-slate-400">Model Confidence</span>
          <div className="text-sm font-semibold text-slate-200 mt-0.5 flex items-center justify-end gap-1.5">
            <span className={`w-2 h-2 rounded-full ${confidence === 'HIGH' ? 'bg-indigo-400' : confidence === 'MEDIUM' ? 'bg-amber-400' : 'bg-slate-400'
              }`} />
            <span>{confidence} Confidence</span>
          </div>
        </div>
      </div>

      {/* Progress track */}
      <div className="w-full h-3 bg-slate-950 rounded-full overflow-hidden p-0.5 border border-white/5">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${colorClass} transition-all duration-700 ease-out`}
          style={{ width: `${Math.min(Math.max(score, 4), 100)}%` }}
        />
      </div>

      <div className="flex justify-between items-center mt-2 text-[10px] font-mono text-slate-400">
        <span>0 (Clean)</span>
        <span>50 (Suspicious)</span>
        <span>100 (Active Threat)</span>
      </div>
    </div>
  );
}

