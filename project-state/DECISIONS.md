# Decisions Log

**Updated:** 2026-11-03 (Milestones M0 - M6 Active)

## How to record decisions

Use `records/decisions/TEMPLATE_ADR.md` for formal Architecture Decision Records (ADRs). Use this file for lightweight decisions and pending owner choices.

---

## Recorded Architectural Decisions

### ADR-001: Backend Framework Selection
**Date:** 2026-11-03  
**Decision:** Python 3.12 + FastAPI (async).  
**Rationale:** Unmatched security libraries (`idna`, `publicsuffix2`, `cryptography`), ML-readiness, async socket parsing, and native OpenAPI generation.

### ADR-002: Frontend Framework Selection
**Date:** 2026-11-03  
**Decision:** Next.js 15 (App Router) + TypeScript + Tailwind CSS.  
**Rationale:** Server components, enterprise React security headers, instant interactive omnibox, and responsive precision dark UI.

### ADR-003: Deployment & Monorepo Model
**Date:** 2026-11-03  
**Decision:** Monorepo with containerized Docker Compose (PostgreSQL 16, Redis 7, API, Web).  
**Rationale:** Complete local reproducibility without global host environment pollution; isolated `.venv` directory for Python.

### ADR-004: Multi-State Verdict & Honest Uncertainty Model
**Date:** 2026-11-03  
**Decision:** Four distinct verdict states: `MALICIOUS`, `SUSPICIOUS`, `UNKNOWN`, `BENIGN`.  
**Rationale:** Precludes false binary "Safe vs Dangerous" coercion. Upstream provider outages yield `UNKNOWN` (status: `PARTIAL`), never `BENIGN`. Clean destinations display explicit limitation disclosures.

### ADR-005: Threat Intelligence Feed Ingestion & In-Memory Hash Lookup
**Date:** 2026-11-03  
**Decision:** Local canonical hash database (SHA-256) indexing OpenPhish, URLhaus, and local seeds.  
**Rationale:** Microsecond-latency exact lookups; zero user URL leakage to external networks; full provenance tracking (source, reported timestamp, confidence).

### ADR-006: Safe DNS/TLS Inspection & Cryptographic Verdict Verification
**Date:** 2026-11-03  
**Decision:** DNS inspection with SSRF rebinding prevention; peer certificate inspection via TLS handshake; HMAC-SHA256 verdict integrity signatures.  
**Rationale:** Protects against DNS rebinding pivots; verifies certificate expiration without executing untrusted payloads; proves tamper-evidence for browser extension.

### ADR-008: Conventional Tamper-Evident HMAC Logging over Public Blockchain
**Date:** 2026-11-03  
**Decision:** Conventional cryptographic HMAC-SHA256 audit verification (`/api/v1/verify/{id}`).  
**Rationale:** Eliminates gas fees, latency, public ledger privacy leakage, and unnecessary complexity while delivering 100% verifiable tamper-evidence.

---

## Pending Decisions (Owner Review)

### DECISION-002: Cloud Deployment Provider
**Options:** Google Cloud Platform (Cloud Run, Cloud SQL) vs AWS (ECS/Fargate, RDS) vs VPS.  
**Status:** Ready for containerized deployment via `docker-compose.yml` or cloud provider.
