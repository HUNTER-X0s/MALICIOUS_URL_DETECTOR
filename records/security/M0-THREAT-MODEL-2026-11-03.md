# URLSentinel — Threat Model (M0 Initial)

**Methodology:** STRIDE + attack trees + trust boundary analysis  
**Status:** Initial seed model — must be expanded per-component in M2  
**Date:** 2026-11-03  
**Reference:** `docs/04-security/THREAT_MODEL_SEED.md`, `docs/04-security/SAFE_URL_HANDLING.md`, `docs/04-security/SCANNER_ISOLATION_REQUIREMENTS.md`

> [!IMPORTANT]
> This is a planning-phase threat model. Security controls have not been implemented or tested yet. All risks are unmitigated at this time. This model must be updated in M2 with component-specific STRIDE analysis and formal ADRs.

---

## 1. Assets

| Asset | Classification | Risk if compromised |
|---|---|---|
| Submitted URLs | Sensitive (may contain credentials/tokens) | User privacy breach, credential exposure |
| Verdict integrity | Critical | SAFE verdict for malicious URL → user harm |
| Threat intelligence data | Confidential | Feed poisoning → systemic false negatives |
| Signing keys (future M10+) | Critical | Tamper with verdicts without detection |
| API keys / provider credentials | Secret | Service abuse, billing fraud |
| Database (URLs, verdicts, users) | Confidential | Data breach, privacy violation |
| Scanner isolation | Critical | Escape to production infrastructure |
| Browser extension code | Critical | Supply chain attack → user compromise at scale |
| CI/CD pipeline | Critical | Supply chain attack → malicious code injection |
| User accounts (future) | Personal data | Account takeover, data breach |
| Audit logs | Security-critical | Evidence tampering |

---

## 2. Trust boundaries

| Boundary | Crossing | Controls needed |
|---|---|---|
| Internet → Public API | All user URL submissions | TLS, rate limiting, input validation, SSRF guard |
| Public API → Verdict Engine | Parsed URL + job parameters | Service auth, input sanitization |
| Verdict Engine → TI Providers | Provider API calls | Allowlisted endpoints, TLS, provider auth, response validation |
| Verdict Engine → Data Layer | Read/write queries | Parameterized queries, least-privilege DB user, connection pooling |
| Application → Scanner Queue | Scan job dispatch (M9+) | Signed job format, auth, size limits |
| Scanner → Internet | Active URL fetch (M9+) | Default-deny egress, allowlist, DNS/IP validation, no private ranges |
| Scanner → Production | Return sanitized result | Sanitized output schema only; no raw content return |
| Extension → API | Cloud verdict lookup | HTTPS, extension ID auth, rate limiting |
| Extension → User Browser | Content script injection | MV3 sandbox, strict CSP, message validation |
| Admin → Control Plane | Administrative operations | Strong MFA, separate auth, audit log |
| CI/CD → Production | Code deployment | Protected branches, signed artifacts, approval gate |

---

## 3. Threat actors

| Actor | Motivation | Capability |
|---|---|---|
| Phishers/malware operators | Evade detection; submit malicious URLs that get SAFE verdict | Can craft URLs, control DNS, create TLS certs |
| URL bombers / API abusers | Resource exhaustion, cost inflation, rate gaming | Automated tooling, botnets |
| SSRF attackers | Access internal infrastructure via URL submission | Knowledge of cloud metadata endpoints, private ranges |
| Feed poisoners | Inject false positives/negatives into TI feeds | Access to community reporting; provider compromise |
| Supply chain attackers | Compromise extension/npm/python deps | CI infiltration, typosquatting packages |
| Extension update attackers | Push malicious extension update to users | Compromised store account or signing key |
| Insider threats | Sabotage, data exfiltration | Repository access, production access |
| Automated scrapers | Bulk URL scraping, competitive intelligence | Rate abuse, browser automation |
| Prompt injection in fetched content | Override agent instructions via malicious web page text | Embedded instructions in `<title>`, meta tags, page content |

---

## 4. STRIDE analysis by component

### 4.1 URL submission endpoint (Public API)

| Threat | STRIDE | Attack | Mitigation | Status |
|---|---|---|---|---|
| SSRF to internal network | Elevation of privilege | Submit URL pointing to `169.254.169.254`, `10.0.0.1`, `::1`, etc. | SSRF guard: parse host, DNS resolve at submission time + at connection, deny private/reserved/loopback/metadata ranges; regex alone insufficient | NOT YET IMPLEMENTED |
| DoS via large URL batch | Denial of service | Submit 10,000 URLs per second | Rate limiting by IP + API key; queue depth limit; backpressure | NOT YET IMPLEMENTED |
| Input validation bypass | Tampering | Submit malformed URL that bypasses parse → different rendering in worker | Use canonical WHATWG URL parser; differential testing against browser | NOT YET IMPLEMENTED |
| Log injection via URL | Tampering | Inject log statements via URL path or query | Structured logging; never interpolate raw URL into log strings; redact query params | NOT YET IMPLEMENTED |
| Credential exposure in submitted URL | Information disclosure | URL contains password/token in query string; logged or stored | Redact credentials and sensitive query params before storage/logging | NOT YET IMPLEMENTED |

### 4.2 Verdict Engine

| Threat | STRIDE | Attack | Mitigation | Status |
|---|---|---|---|---|
| Feed-failure → SAFE coercion | Tampering | Attacker disrupts TI provider; system returns BENIGN | Rule: provider failure or timeout → UNKNOWN or PARTIAL; never BENIGN | NOT YET IMPLEMENTED |
| Adversarial URL evasion | Spoofing | Craft URL that evades lexical rules (encoding, IDN, subdomain confusion) | Canonical normalization + differential tests + adversarial test corpus | NOT YET IMPLEMENTED |
| Score inflation from correlated signals | Tampering | Double-count signals from same source, artificially inflate confidence | Evidence deduplication; signal independence tracking | NOT YET IMPLEMENTED |
| False positive on legitimate URL | Repudiation | Legitimate business URL flagged MALICIOUS | False-positive report mechanism; analyst review queue; human-in-loop for high-impact verdicts | NOT YET IMPLEMENTED |

### 4.3 Threat intelligence ingestion

| Threat | STRIDE | Attack | Mitigation | Status |
|---|---|---|---|---|
| Feed poisoning | Tampering | Attacker injects false positives into community feed | Multi-source corroboration; source confidence weighting; TTL and freshness checks | NOT YET IMPLEMENTED |
| Provider compromise | Spoofing | TI provider serves adversarial data | TLS + certificate pinning (where feasible); response validation; anomaly detection on feed delta | NOT YET IMPLEMENTED |
| Stale data as SAFE signal | Information disclosure | Old data used after threat expires or was a false positive | Mandatory freshness TTL; explicit expiry; staleness = UNKNOWN not BENIGN | NOT YET IMPLEMENTED |
| Prompt injection in feed content | Tampering | Malicious feed entry contains agent instructions | Treat all feed data as untrusted; parse only expected schema fields; do not evaluate free-text as instructions | NOT YET IMPLEMENTED |

### 4.4 Isolated Scanner (M9 — future)

| Threat | STRIDE | Attack | Mitigation | Status |
|---|---|---|---|---|
| Scanner-to-host escape | Elevation of privilege | Exploit VM/container breakout to reach production | microVM isolation (Firecracker or equivalent); no shared kernel without additional isolation; independent security review required | DESIGN ONLY |
| SSRF through scanner | Elevation of privilege | Scanner fetches internal metadata endpoint via redirect | DNS validation per hop; IP check at connection time; deny private/reserved/metadata ranges | DESIGN ONLY |
| DNS rebinding | Spoofing | Hostname resolves to public IP at validation, then private IP at connection | IP pinning / connection-time revalidation; resolver controls | DESIGN ONLY |
| Resource exhaustion in scanner | Denial of service | Malicious page causes infinite redirect, huge DOM, infinite loop | Hard limits: redirect count (max 10), response size (max 10MB), execution time (max 60s), CPU, memory | DESIGN ONLY |
| Artifact persistence (malware) | Tampering | Scanner writes malware to shared storage | Quarantine only; no execution outside scanner; artifact deletion after analysis; virus scan output | DESIGN ONLY |
| Production credentials in scanner | Elevation of privilege | Scanner process has access to DB credentials | Scanner has zero production credentials; separate secret store; minimal egress only | DESIGN ONLY |

### 4.5 Browser Extension

| Threat | STRIDE | Attack | Mitigation | Status |
|---|---|---|---|---|
| Extension supply chain attack | Tampering | Malicious npm package in extension build | Pin dependencies; SCA scanning; SBOM; signed extension package | NOT YET IMPLEMENTED |
| Content script injection attack | Elevation of privilege | Attacker page exploits content script to escalate | MV3 isolation; strict CSP; message origin validation; minimal content script surface | NOT YET IMPLEMENTED |
| Message spoofing | Spoofing | Malicious page sends fake chrome.runtime message | Validate sender origin; explicit message schema; allowlist message types | NOT YET IMPLEMENTED |
| Remote code execution via extension | Tampering | `eval()` or remote script injection | Banned in MV3; CSP `script-src 'self'`; no `innerHTML` from network | NOT YET IMPLEMENTED |
| Browsing history collection | Information disclosure | Extension over-collects URLs | Request only necessary permissions; no `tabs.query` without user action; no persistent URL log | NOT YET IMPLEMENTED |

---

## 5. Attack paths (high-priority)

### Path 1: SSRF to cloud metadata (CRITICAL)
1. Attacker submits URL `http://169.254.169.254/latest/meta-data/`
2. URL passes scheme check (HTTPS/HTTP)
3. No SSRF guard in place → API service makes HTTP request to metadata endpoint
4. Cloud credentials leaked from metadata service
5. **Impact:** Full cloud account compromise
6. **Mitigation:** Parse destination IP at submission time AND at connection time; deny 169.254.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, ::1, fc00::/7, fe80::/10, ::ffff:0:0/96

### Path 2: Feed poisoning → false negative
1. Attacker submits false "legitimate" verdicts to community reporting (M10+)
2. Newly created phishing domain gets community BENIGN labels
3. Verdict engine trusts community labels with insufficient corroboration
4. Phishing URL serves as BENIGN/LOW_RISK → users proceed to phishing page
5. **Impact:** Systematic harm to users trusting URLSentinel
6. **Mitigation:** Multi-source corroboration required; community labels weighted low without analyst verification; freshness TTL

### Path 3: Extension supply chain
1. Attacker creates typosquatted npm package near a dependency
2. Developer or CI installs malicious package
3. Extension build includes malicious code
4. Extension update pushed to users via Chrome Web Store
5. **Impact:** Attacker code runs in all users' browsers with extension permissions
6. **Mitigation:** Lock dependencies with exact versions; SCA scanning in CI; code review of dependency updates; signed extension package

### Path 4: Coerced SAFE verdict via provider outage
1. Attacker launches DoS against TI provider
2. URLSentinel cannot reach provider; system falls back to BENIGN
3. Malicious URLs return SAFE during outage window
4. **Impact:** Users harmed; product trust destroyed
5. **Mitigation:** Provider failure → UNKNOWN/PARTIAL; cached last-known good verdict with freshness TTL; multiple provider sources

---

## 6. Risk register (initial)

| ID | Risk | Likelihood | Impact | Severity | Mitigation | Owner |
|---|---|---|---|---|---|---|
| RISK-001 | SSRF to internal infrastructure | HIGH (no guard yet) | CRITICAL | CRITICAL | SSRF guard subsystem in M3 | Security Engineering |
| RISK-002 | Scanner escape to production | MEDIUM (not built yet) | CRITICAL | HIGH | Full scanner trust-zone design + independent review before M9 | Security Engineering |
| RISK-003 | TI provider licensing violation | HIGH (no license review) | HIGH | HIGH | Legal/license review in M1 before M5 integration | Product + Legal |
| RISK-004 | Feed poisoning → false negatives | MEDIUM | HIGH | HIGH | Multi-source corroboration; source confidence tracking | Threat Detection |
| RISK-005 | Extension supply chain attack | MEDIUM | CRITICAL | HIGH | Pinned deps, SCA, signed package | DevSecOps |
| RISK-006 | Provider outage → SAFE coercion | HIGH (rule not yet coded) | HIGH | HIGH | UNKNOWN on failure rule enforced before M5 | Backend Engineering |
| RISK-007 | URL/credential leakage in logs | HIGH (no redaction yet) | HIGH | HIGH | Log redaction in M3 | Backend Engineering |
| RISK-008 | DNS rebinding in scanner | MEDIUM | HIGH | HIGH | IP pinning in scanner design, M2 | Security Engineering |
| RISK-009 | Adversarial URL evasion | MEDIUM | MEDIUM | MEDIUM | Adversarial test corpus in M4 | Detection Engineering |
| RISK-010 | Misleading SAFE UI message | MEDIUM | HIGH | HIGH | UX/copy review; no green "safe" badge without appropriate caveats | UX + Security |
| RISK-011 | Prompt injection via feed/page content | MEDIUM | MEDIUM | MEDIUM | Treat all external content as untrusted data; schema-only parsing | All Engineering |
| RISK-012 | Compliance gap (DPDPA/GDPR) | MEDIUM | HIGH | HIGH | Legal review in M1 before launch | Legal + Privacy |
| RISK-013 | ML training data poisoning (M8+) | LOW (ML not yet planned) | HIGH | MEDIUM | Domain-grouped splits, leakage controls, OOD testing | ML Engineering |
| RISK-014 | Blockchain key compromise (if used) | LOW (not in MVP) | CRITICAL | MEDIUM | Defer blockchain until need proven; use conventional tamper-evident log | Architecture |
| RISK-015 | Cryptographic signing key compromise | LOW (not in MVP) | CRITICAL | MEDIUM | HSM evaluation in M2; key rotation design before M10 | Security Engineering |

---

## 7. SSRF prevention subsystem specification

> This is a critical, standalone security subsystem — not an afterthought.

**Required controls (must be implemented before any network-touching feature):**

1. **URL parsing** — parse host component using WHATWG URL standard; extract hostname
2. **Scheme allowlist** — accept only `https://` and `http://` for URL analysis; reject all others
3. **Port restriction** — default: allow only 80, 443, 8080, 8443; deny all others unless explicitly justified
4. **DNS resolution** — resolve hostname using controlled resolver; validate all A/AAAA records
5. **IP validation (after DNS)** — deny:
   - IPv4: 0.0.0.0/8, 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.168.0.0/16, 198.18.0.0/15, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 240.0.0.0/4, 255.255.255.255/32
   - IPv6: ::1, fc00::/7, fe80::/10, ::ffff:0:0/96 (IPv4-mapped), 2001:db8::/32, 64:ff9b::/96
   - Cloud metadata: 169.254.169.254 (AWS/GCP/Azure), 100.100.100.200 (Alibaba Cloud)
6. **Numeric IP notation** — parse and validate decimal, hex, octal, and dotted-decimal IP variants
7. **Redirect validation** — re-resolve and re-validate at every redirect hop; do not trust initial validation alone
8. **No DNS rebinding** — record resolved IP at first connection; reject if IP changes on reconnect
9. **Never use regex alone** — regex cannot reliably catch all SSRF bypass variants

**Test requirements:**
- Test every private/reserved range listed above
- Test IPv4-in-IPv6 representation (e.g., `::ffff:10.0.0.1`)
- Test octal notation (e.g., `0177.0.0.1` = 127.0.0.1)
- Test hex notation (e.g., `0x7f000001` = 127.0.0.1)
- Test URL with credentials in userinfo (`http://attacker:@169.254.169.254/`)
- Test DNS rebinding via short TTL
- Test redirect chain that transitions from public to private IP
- Test `file://`, `javascript:`, `data:`, `gopher://` schemes

