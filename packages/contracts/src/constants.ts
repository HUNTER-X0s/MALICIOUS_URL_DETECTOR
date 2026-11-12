/**
 * URLSentinel Constants and Design Tokens
 */

export const API_VERSION = 'v1';
export const CONTRACT_VERSION = '1.0.0';

export const MAX_URL_LENGTH = 2048;

export const VERDICT_CONFIG = {
  MALICIOUS: {
    label: 'Malicious Destination',
    severity: 'danger',
    colorHex: '#ef4444',
    bgHex: 'rgba(239, 68, 68, 0.12)',
    borderHex: 'rgba(239, 68, 68, 0.3)',
    defaultAction: 'Do not proceed to this website. Active deception or malware delivery detected.',
  },
  SUSPICIOUS: {
    label: 'Suspicious Indicators',
    severity: 'warning',
    colorHex: '#f59e0b',
    bgHex: 'rgba(245, 158, 11, 0.12)',
    borderHex: 'rgba(245, 158, 11, 0.3)',
    defaultAction: 'Exercise extreme caution. Do not enter credentials, financial information, or download files.',
  },
  UNKNOWN: {
    label: 'Inconclusive / Unknown',
    severity: 'neutral',
    colorHex: '#94a3b8',
    bgHex: 'rgba(148, 163, 184, 0.12)',
    borderHex: 'rgba(148, 163, 184, 0.3)',
    defaultAction: 'Insufficient threat evidence available. Treat link with standard caution and verify author.',
  },
  BENIGN: {
    label: 'No Known Threats Found',
    severity: 'success',
    colorHex: '#10b981',
    bgHex: 'rgba(16, 185, 129, 0.12)',
    borderHex: 'rgba(16, 185, 129, 0.3)',
    defaultAction: 'No active threat records or anomalous markers found. Note: absolute safety cannot be guaranteed.',
  },
} as const;

export const HIGH_VALUE_BRANDS = [
  'google',
  'microsoft',
  'apple',
  'amazon',
  'paypal',
  'netflix',
  'facebook',
  'instagram',
  'whatsapp',
  'chase',
  'wellsfargo',
  'bankofamerica',
  'citibank',
  'binance',
  'coinbase',
  'github',
  'dropbox',
  'adobe',
  'linkedin',
  'twitter',
  'steam',
] as const;

export const KNOWN_URL_SHORTENERS = [
  'bit.ly',
  'tinyurl.com',
  't.co',
  'goo.gl',
  'ow.ly',
  'is.gd',
  'buff.ly',
  'adf.ly',
  'bit.do',
  'mcaf.ee',
  'rebrand.ly',
  'cutt.ly',
  'shorturl.at',
] as const;

export const SENSITIVE_QUERY_PARAMS = [
  'token',
  'access_token',
  'auth',
  'key',
  'api_key',
  'password',
  'pwd',
  'secret',
  'client_secret',
  'session',
  'session_id',
  'jwt',
  'refresh_token',
  'code',
  'passcode',
  'pin',
] as const;

