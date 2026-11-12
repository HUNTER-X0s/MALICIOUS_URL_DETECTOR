# ADR-006: Safe DNS/TLS Inspection and Cryptographic Verdict Integrity

**Status:** ACCEPTED  
**Date:** 2026-11-03  
**Deciders:** URLSentinel Autonomous Engineering  
**Consulted:** Security Engineering, Backend Engineering

---

## Context
1. Modern phishing operations heavily utilize TLS/SSL encryption to create a false sense of security. Users and naive scanners frequently confuse "HTTPS connection" with "Safe destination".
2. Scanning destinations that resolve dynamically poses a risk of DNS Rebinding attacks (where a hostname initially resolves to a public IP to pass safety checks, but on subsequent connections resolves to an internal/loopback/cloud metadata IP).
3. If verdict responses are transmitted across untrusted networks or cached on intermediate proxies, a compromised network could tamper with the verdict, converting `MALICIOUS` to `BENIGN`.

## Decision
1. **Safe DNS & Rebinding Defense**:
   - Implement `inspect_dns_records` in `dns_tls_inspector.py`.
   - Every resolved A and AAAA address is strictly verified against `ssrf_guard`.
   - Any resolution to loopback, RFC 1918, or cloud metadata immediately raises `SSRFBlockedError`.
2. **TLS Certificate Inspection**:
   - Non-hostile TLS handshake extracts peer certificate validity without downloading web page bodies.
   - Extracts issuer, expiry date, days remaining, and Subject Alternative Names (SANs).
   - Validates that expired certificates or domain mismatches are recorded as elevated risk signals.
   - Explicit invariant documented in evidence: *Valid TLS does NOT imply safe intent*.
3. **Cryptographic Verdict Verification (`/api/v1/verify/{scan_id}`)**:
   - Computes an HMAC-SHA256 signature over a canonical envelope: `{scan_id}:{url_hash}:{verdict}:{risk_score}:{checked_at}:v1`.
   - Proves tamper-evidence to the browser extension and external verifiers without the overhead of public blockchain transactions.

## Consequences
- **Positive:** Immune to DNS rebinding; accurate certificate expiration tracking; provable integrity against verdict manipulation.
- **Negative:** TLS handshake adds 50–300ms if certificate validation is requested.

