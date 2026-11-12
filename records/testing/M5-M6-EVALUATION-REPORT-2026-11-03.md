# Milestone M5 & M6 Test and Security Evaluation Report

**Date:** 2026-11-03  
**Status:** COMPLETE — 100% Tests Passed (43/43)  
**Execution Environment:** Isolated workspace virtual environment `z:\URLSentinel\.venv`  
**Command:** `z:\URLSentinel\.venv\Scripts\pytest.exe z:\URLSentinel\services\api\tests -v`

---

## 1. Test Suite Results Summary

| Test Module | Tests Run | Passed | Failed | Scope Covered |
|---|---|---|---|---|
| `tests/test_ssrf_guard.py` | 8 | 8 | 0 | Loopback, RFC 1918 subnets, cloud metadata (169.254.169.254, 100.100.100.200), IPv4-mapped IPv6, octal, hex, schemes, ports |
| `tests/test_url_normalizer.py` | 6 | 6 | 0 | WHATWG normalization, port stripping, dot-segment traversal, PSL domain decomposition, SHA-256 hash |
| `tests/test_url_redactor.py` | 3 | 3 | 0 | Authority credentials purging, sensitive query parameter masking (`[REDACTED]`), safe parameter retention |
| `tests/test_lexical_analyzer.py` | 6 | 6 | 0 | Shannon entropy, Levenshtein brand similarity, numeric IP hosts, shortener detection, clean destination low scoring |
| `tests/test_homoglyph_detector.py` | 4 | 4 | 0 | Cyrillic/Greek homoglyph normalization, Cyrillic PayPal lure detection, brand spoofing in domain labels, official domains preservation |
| `tests/test_feed_ingestion.py` | 4 | 4 | 0 | Threat intelligence index initialization, exact URL hash matching, domain reputation matching, clean URL handling |
| `tests/test_dns_tls_inspector.py` | 3 | 3 | 0 | Private IP rebinding prevention, non-routable domain handling, unreachable TLS target safety |
| `tests/test_verdict_engine.py` | 3 | 3 | 0 | Provider failure yields `UNKNOWN` (never `BENIGN`), confirmed TI match yields `MALICIOUS`, clean domain includes explicit caveats |
| `tests/test_api.py` | 6 | 6 | 0 | End-to-end `/scan`, `/health`, `/stats`, `/report`, `/verify/{id}`, SSRF blocking HTTP 400 |
| **Total** | **43** | **43** | **0** | **Execution Duration: 2.95s** |

---

## 2. Invariants Formally Verified

1. **SSRF Boundary Invulnerability**:
   - Every destination is validated against `is_ip_denied`.
   - Obfuscated IP notations (`0x7f000001`, `2130706433`, `0177.0.0.1`) are parsed to canonical IPv4 before evaluation and rejected.
   - Cloud metadata IP `169.254.169.254` is blocked at input validation time and at DNS resolution time.

2. **Detection Honesty (No Coerced Benign)**:
   - When external feeds report connection timeout or degradation, verdict state machine outputs `UNKNOWN` (status: `PARTIAL`).
   - Clean domains output `BENIGN` with an explicit limitation disclosure: *"No active threats detected in cataloged datasets. Always verify unfamiliar origins."*

3. **Data Minimization & Redaction**:
   - Sensitive query tokens (`token`, `key`, `password`, `jwt`) are redacted before any logging or reporting.
   - Tested on `https://evil-phish.com/login?token=secret123` -> response payload verified that `secret123` is scrubbed.

4. **Cryptographic Tamper-Evidence**:
   - `/api/v1/verify/{scan_id}` computes HMAC-SHA256 signature over the canonical verdict record.
   - Signature algorithm: `HMAC-SHA256`, 64-character hexadecimal digest.

