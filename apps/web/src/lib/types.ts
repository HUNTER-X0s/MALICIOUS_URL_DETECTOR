export type Verdict = 'MALICIOUS' | 'SUSPICIOUS' | 'UNKNOWN' | 'BENIGN';

export type ScanStatus =
  | 'QUEUED'
  | 'RUNNING'
  | 'COMPLETED'
  | 'PARTIAL'
  | 'FAILED'
  | 'EXPIRED';

export type Confidence = 'LOW' | 'MEDIUM' | 'HIGH';

export interface EvidenceItem {
  id: string;
  layer: string;
  signal_name: string;
  source: string;
  observed_at: string;
  freshness: string;
  contribution: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFORMATIONAL';
  description: string;
  technical_details?: Record<string, unknown>;
}

export interface TechnicalDetails {
  scheme: string;
  host: string;
  port?: number | null;
  path: string;
  query_params_count: number;
  entropy: number;
  is_ip_host: boolean;
  is_shortener: boolean;
  suspicious_tokens: string[];
  typosquatting_matches: string[];
  punycode?: string | null;
  resolved_ips?: string[];
}

export interface VerdictResult {
  id: string;
  url: string;
  url_hash: string;
  verdict: Verdict;
  status: ScanStatus;
  risk_score: number;
  confidence: Confidence;
  summary: string;
  evidence: EvidenceItem[];
  limitations: string[];
  technical_details: TechnicalDetails;
  recommended_action: string;
  checked_at: string;
  expires_at: string;
  contract_version: string;
}

export interface SystemStats {
  total_scans_today: number;
  threats_detected_today: number;
  average_latency_ms: number;
  active_rules_count: number;
  last_feed_sync: string;
  clean_scans_today?: number;
  ssrf_blocks_today?: number;
  engine_status?: string;
  uptime_seconds?: number;
  last_scan_at?: string;
  subsystems?: Record<string, string>;
}

