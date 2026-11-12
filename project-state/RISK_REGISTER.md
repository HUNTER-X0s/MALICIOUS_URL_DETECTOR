# Risk Register

**Updated:** 2026-11-03 (Implementation Phase)  
**Detail:** Full threat model in `records/security/M0-THREAT-MODEL-2026-11-03.md`

## Risk Status

| ID | Risk | Severity | Status | Verified Mitigation & Code Location |
|---|---|---|---|---|
| RISK-001 | SSRF to cloud infrastructure via URL submission | **CRITICAL** | **MITIGATED & TESTED** | `services/api/src/urlsentinel/core/ssrf_guard.py` — blocks all private IPv4, IPv6, cloud metadata, octal/hex encodings. Verified by 8 automated unit tests. |
| RISK-002 | Scanner escape to production (M9+) | HIGH | DESIGN ONLY | Isolated scanner trust zone designed; execution gated until Phase 2. |
| RISK-003 | TI provider licensing violation | HIGH | UNRESOLVED | Legal review scheduled for commercial licensing (Google Web Risk vs Safe Browsing). |
| RISK-004 | Feed poisoning → false negatives | HIGH | MITIGATED | Multi-source corroboration required in `verdict_engine.py`; community labels cannot override confirmed feeds. |
| RISK-005 | Extension supply chain attack | HIGH | MITIGATED | Extension is pure zero-dependency vanilla JS/CSS/HTML with strict CSP (`script-src 'self'`). |
| RISK-006 | Provider outage → SAFE/BENIGN coercion | HIGH | **MITIGATED & TESTED** | Enforced in `verdict_engine.py`. Provider error yields `UNKNOWN` (status: `PARTIAL`), never `BENIGN`. Verified by `test_verdict_engine.py`. |
| RISK-007 | URL/credential leakage in logs | HIGH | **MITIGATED & TESTED** | `url_redactor.py` strips authority credentials and masks sensitive query parameters (`token`, `key`, `password`). Verified by `test_url_redactor.py`. |
| RISK-009 | Adversarial URL evasion & typosquatting | MEDIUM | **MITIGATED & TESTED** | `lexical_analyzer.py` calculates Levenshtein distance against high-value brands, Shannon entropy, and IDN homoglyphs. Verified by `test_lexical_analyzer.py`. |
| RISK-010 | Misleading UI safety messaging | HIGH | **MITIGATED** | Web app & extension display explicit limitations and honest caveats: "No system can guarantee 100% safety." |
| RISK-011 | Prompt injection via untrusted content | MEDIUM | MITIGATED | Free text in incoming URLs is strictly treated as untrusted data; never evaluated as code or instructions. |
