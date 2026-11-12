/**
 * URLSentinel Shared Contract Types
 * Version: v1
 */

export type Verdict = 'MALICIOUS' | 'SUSPICIOUS' | 'UNKNOWN' | 'BENIGN';

export type ScanStatus =
  | 'QUEUED'
  | 'RUNNING'
  | 'COMPLETED'
  | 'PARTIAL'
  | 'FAILED'
  | 'EXPIRED';

export type Confidence = 'LOW' | 'MEDIUM' | 'HIGH';

export type SignalContribution = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFORMATIONAL';

export interface EvidenceItem {
  id: string;
  layer: 'exact_reputation' | 'structure' | 'lexical' | 'host_domain' | 'dns' | 'tls' | 'threat_intel' | 'behavioral' | 'heuristics';
  signal_name: string;
  source: string;
  observed_at: string;
  freshness: string;
  contribution: SignalContribution;
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
  risk_score: number; // 0 - 100
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

export interface ScanRequest {
  url: string;
  client_id?: string;
  request_deep_scan?: boolean;
}

export interface ScanErrorResponse {
  error: string;
  code: string;
  message: string;
  details?: Record<string, unknown>;
  timestamp: string;
}

export interface HealthCheckResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  version: string;
  timestamp: string;
  services: {
    database: 'up' | 'down' | 'degraded';
    redis: 'up' | 'down' | 'degraded';
    threat_intel: 'up' | 'down' | 'degraded';
  };
}

export interface SystemStatsResponse {
  total_scans_today: number;
  threats_blocked_today: number;
  average_latency_ms: number;
  active_rules_count: number;
  last_feed_sync: string;
}

