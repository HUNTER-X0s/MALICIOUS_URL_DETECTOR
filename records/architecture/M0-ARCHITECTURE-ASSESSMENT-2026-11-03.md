# URLSentinel — Architecture Assessment (M0)

**Status:** Initial recommendation — hypothesis until validated through threat modeling, load testing, and operational exercises  
**Date:** 2026-11-03  
**Authority:** System Architecture and Engineering Leadership function  
**Reference:** `docs/03-architecture/ARCHITECTURE_PRINCIPLES.md`, `docs/03-architecture/REFERENCE_SYSTEM_CONTEXT.md`

---

## 1. Recommended initial architecture

### 1.1 Overarching approach

**Modular monolith with isolated workers** — not microservices.

The blueprint's section 102 shows a multi-zone architecture with CDN/WAF, API gateway, fast/deep analysis paths, risk engine, and scanner isolation. This is the right *eventual* target. For M3–M7, the recommended approach is a well-structured monolith with explicit domain boundaries, deployed as a single service with one or two isolated worker types. Services split only when a measurable requirement (scale, isolation, team boundary, distinct deployment lifecycle) justifies it.

**Rationale:**
- No existing user load to justify premature distributed complexity
- Microservices require distributed tracing, service mesh, distributed secrets, distributed auth, cross-service contract testing, and ops overhead that a 0→1 startup cannot sustain
- Modular boundaries (URL parsing, verdict logic, feed ingestion, caching) can be honored within a well-structured monolith and extracted later without architectural rework
- Precedent: `docs/03-architecture/ARCHITECTURE_PRINCIPLES.md` principle 1 explicitly states "modular monolith/API" unless measurable requirements justify distributed services

### 1.2 Recommended technology stack

> [!WARNING]
> These are initial recommendations. Technology choices require ADRs with explicit alternatives, tradeoffs, and rationale before adoption. No framework is selected merely because it is fashionable.

| Layer | Recommendation | Rationale |
|---|---|---|
| **Backend language** | Python 3.12 or TypeScript/Node.js 24 | Both are present in environment. Python has strong security/ML library ecosystem. TypeScript provides end-to-end type safety if shared with frontend. Decision requires ADR. |
| **Backend framework** | FastAPI (Python) or Hono (TypeScript) | Modern, minimal, async, OpenAPI-native, well-maintained. Alternatives: Django REST Framework (Python), Express (Node). |
| **Frontend** | Next.js (App Router) + TypeScript | SSR/SSG for SEO and performance, React component model, strong ecosystem, Vercel-native. Alternative: SvelteKit (smaller bundle, simpler model). Requires ADR. |
| **Browser extension** | TypeScript + Manifest V3 | MV3 is the current Chrome/Edge requirement. Separate build from web app. No remote executable code. |
| **Primary database** | PostgreSQL | Relational, ACID, excellent JSON support (JSONB), strong ecosystem, manageable backup/restore. |
| **Cache / fast-path** | Redis | In-memory lookups for known-bad URL hashes, domain reputation, feed results. |
| **Message queue** | Redis Streams (initial) → BullMQ or Celery | For scan job queuing. Redis Streams is lightweight for MVP. Named queue system for worker separation. |
| **Object storage** | S3-compatible (MinIO local dev, cloud provider in prod) | Scan artifacts, reports, feed snapshots. |
| **Secret management** | Environment-injected secrets via CI (dev) → Cloud KMS/Secret Manager (prod) | Never in repo. Never in browser code. |
| **Observability** | OpenTelemetry + Prometheus + Grafana (or cloud-native equivalent) | Structured logs, metrics, traces. |
| **CI/CD** | GitHub Actions | Protected branches, automated gates. |
| **Containerization** | Docker (dev parity) | Not Kubernetes for MVP. Single-node deployment initially. |

### 1.3 System context diagram (text)

```
                           ┌──────────────────────────────┐
                           │         USERS                │
                           │  Browser + Extension         │
                           └────────────┬─────────────────┘
                                        │ HTTPS
                           ┌────────────▼─────────────────┐
                           │      CDN / Edge (Cloudflare) │
                           │   TLS termination, WAF,      │
                           │   DDoS protection, caching   │
                           └────────────┬─────────────────┘
                                        │
                           ┌────────────▼─────────────────┐
                           │       Public API             │
                           │   (Rate limit, auth check,   │
                           │    input validation)         │
                           │   Trust boundary: PUBLIC     │
                           └────┬──────────────┬──────────┘
                                │              │
               ┌────────────────▼──┐    ┌──────▼─────────────────┐
               │   FAST PATH       │    │     DEEP PATH (Queued)  │
               │  URL parsing      │    │  Isolated worker        │
               │  Lexical signals  │    │  (M9 only, after gate)  │
               │  Cache lookup     │    │  Disposable VM/sandbox  │
               │  TI reputation    │    │  Default-deny egress    │
               │  Domain/DNS/TLS   │    └─────────────────────────┘
               │  Rule-based score │
               └────────┬──────────┘
                        │
               ┌────────▼──────────────────────────────────┐
               │            VERDICT ENGINE                  │
               │   Multi-signal aggregation                │
               │   Evidence traceability                   │
               │   Confidence + uncertainty propagation    │
               │   MALICIOUS / SUSPICIOUS / UNKNOWN /      │
               │   BENIGN — never coerce unknowns to BENIGN│
               └──────────────┬────────────────────────────┘
                              │
               ┌──────────────▼────────────────────────────┐
               │          DATA LAYER                        │
               │  PostgreSQL (primary, structured data)    │
               │  Redis (cache, fast-path lookups)         │
               │  Object storage (artifacts, feed snaps)   │
               │  Trust boundary: DATA                     │
               └────────────────────────────────────────────┘
```

### 1.4 Trust zones

| Zone | Components | Trust level | Egress |
|---|---|---|---|
| Public | CDN/WAF, API gateway | Untrusted — validate everything | Internet ← inbound only |
| Application | API service, verdict engine, worker scheduler | Medium — authenticated service identities | Outbound to TI providers (allowlisted) |
| Data | PostgreSQL, Redis, object storage | High — no direct external access | None (accessed only from Application zone) |
| Scanner | Disposable VM/container | Minimal — no production credentials | Allowlisted external only; deny all private/loopback/metadata |
| Admin | Admin control plane | Highest — strong MFA required | Restricted; audit everything |

### 1.5 Key architectural decisions pending (ADRs needed)

| Decision | Options | Risk if deferred |
|---|---|---|
| ADR-001: Backend language (Python vs TypeScript) | Python 3.12 / TypeScript + Node | Inconsistent stack; integration overhead |
| ADR-002: Frontend framework | Next.js vs SvelteKit | UI rework if wrong choice |
| ADR-003: Deployment target | Managed cloud (GCP/AWS/Azure) vs VPS | Ops burden, scaling limits |
| ADR-004: Verdict schema (labels, versioning, signing) | MALICIOUS/SUSPICIOUS/UNKNOWN/BENIGN vs richer set | Breaking API changes later |
| ADR-005: Threat intelligence provider selection | Google Web Risk + URLhaus + others | Licensing violation, coverage gaps |
| ADR-006: Scanner isolation technology | microVM (Firecracker) vs gVisor vs container-only vs cloud workload sandbox | Scanner escape vulnerability |
| ADR-007: Auth provider | Custom JWT vs Auth0/Clerk/Firebase vs Cognito | Auth vulnerabilities, migration cost |
| ADR-008: Blockchain (section 023) | Conventional tamper-evident log vs public blockchain | Complexity, cost, governance |

---

## 2. URL parsing and normalization

**Non-negotiable requirements from knowledge base:**
- Use WHATWG URL standard (not RFC 3986 alone; browsers use WHATWG)
- Parse without network access
- Handle: IPv4 variants, IPv6 literals, IDN/Punycode, Unicode confusables, percent-encoding, backslashes, dot segments, userinfo, port ranges, alternate schemes
- Differential testing against browser URL behavior
- Redact query parameters in logs/analytics
- Libraries: Python `urllib.parse` + `ada-url` or `furl`; JavaScript: WHATWG `URL` API; validate with `publicsuffix2`/`tldextract`

---

## 3. Detection pipeline

**Layered evaluation order (fast to slow):**

1. **Scheme check** — reject `file://`, `javascript:`, `data:`, non-HTTP/HTTPS (unless explicit purpose defined)
2. **SSRF destination check** — before any network operation: deny private, loopback, link-local, reserved, metadata IP ranges (IPv4 + IPv6-mapped)
3. **Exact URL hash lookup** — Redis cache of known-bad URL hashes (bloom filter for "fast miss" in extension)
4. **Domain/IP reputation** — licensed TI provider lookup (Google Web Risk or equivalent)
5. **Lexical analysis** — URL structure entropy, length, suspicious patterns, typosquatting signals
6. **DNS/domain signals** — domain age, registration evidence, DNS anomalies (controlled query)
7. **TLS/certificate** — certificate validity, age, hostname match, CT log presence
8. **Rule-based scoring** — weighted combination of signals above
9. **ML model** (M8+) — only after trained, evaluated, and calibrated model approved
10. **Verdict aggregation** — MALICIOUS / SUSPICIOUS / UNKNOWN / BENIGN with evidence + confidence

**Verdict rules (non-negotiable):**
- Feed failure → UNKNOWN, not BENIGN
- Provider timeout → UNKNOWN or PARTIAL
- Missing DNS → flag; do not upgrade to MALICIOUS on absence alone
- HTTPS presence → explicitly NOT a safety signal
- Zero hits → UNKNOWN (no known threat), not SAFE

---

## 4. Browser extension

**MV3 architecture:**
- Service worker (background): local cache, verdict lookup, navigation event handler
- Content scripts: minimal — inject warning overlay only when verdict = MALICIOUS/SUSPICIOUS
- Popup: current site status, report button, settings
- Storage: chrome.storage.local for cache (encrypted); no sync of URLs
- Permissions: `declarativeNetRequest`, `webNavigation`, `storage`, `activeTab` — minimum required
- No remote code execution (`eval`, `Function()`, `innerHTML` from network)
- All external resources: served from declared extension bundle only
- Message validation: strict schema validation on all chrome.runtime messages
- Update channel: Chrome Web Store only; no side-loading for production

---

## 5. Storage and retention

| Data type | Storage | Default retention | Justification |
|---|---|---|---|
| Submitted URL (normalized) | PostgreSQL (hashed) | 30 days | Rate limiting, dedup, analytics |
| Verdict + evidence | PostgreSQL | 90 days (configurable) | Result lookup, audit |
| Raw submitted URL string | NOT STORED by default | N/A | Privacy — may contain credentials, tokens |
| Scan artifacts (screenshots etc.) | Object storage | 7 days | Sandboxed; M9 only |
| Feed data | Object storage | Per-provider retention rules | Provider licensing compliance |
| Audit log | PostgreSQL (append-only) | 2 years | Security, compliance |
| User accounts | PostgreSQL | Until deletion | DPDPA/GDPR compliance |

> [!CAUTION]
> Query parameters and fragments often contain session tokens, password reset tokens, and personal identifiers. These must be redacted before storage, logging, or telemetry.

---

## 6. Privacy and data governance

- **Data minimization:** collect only what is necessary for the detection function
- **URL redaction:** strip credentials, tokens, and sensitive query parameters before logging
- **Default anonymization:** no user-identifiable URL storage without disclosure and consent
- **Retention controls:** automated deletion jobs; hard TTL on scan records
- **External transfers:** explicit allowlist of providers; no URL submitted to external providers without disclosure in privacy policy
- **Extension:** no persistent browsing history; verdict cache expires; no upload of full URL without user trigger
- **Legal research required:** India DPDPA (2023), GDPR (if EU users), CCPA (if CA users) before launch

---

## 7. Deployment and operations

**Initial deployment model (M12 target):**
- Single cloud provider (TBD by ADR-003)
- Infrastructure-as-code from M3
- Dev → Staging → Production pipeline with approval gate on production
- Environment separation: dev (local containers), staging (cloud), prod (cloud)
- Database: managed PostgreSQL with automated backups and point-in-time recovery
- Secrets: cloud-native secret manager (never in `.env` files in staging/prod)
- Monitoring: OpenTelemetry → cloud-native metrics, alerting
- Rollback: database migration rollback scripts required for every migration
- Extension: Chrome Web Store publishing requires explicit owner approval

---

## 8. Observability requirements

**Minimum for M3:**
- Structured JSON logs (no raw URL strings in logs)
- P50/P95/P99 API latency per endpoint
- Error rates and status codes
- Queue depth and processing age
- Cache hit ratio (extension, Redis)
- Threat-feed freshness (last successful update per provider)
- Scanner health (M9+)

**M7+ additions:**
- Detection quality metrics (FP rate, FN rate from labeled set)
- False-positive report rate from users
- Extension install/active user counts (privacy-respecting aggregates only)

