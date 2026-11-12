# URLSentinel — Dependency-Aware Implementation Roadmap (M0)

**Status:** Initial roadmap based on M0 audit findings — must be validated and refined in M1–M2  
**Date:** 2026-11-03  
**Authority:** `docs/12-roadmap/ROADMAP_METHOD.md`, `docs/01-product/FEATURE_TRACEABILITY_103.md`

---

## Roadmap summary

| Milestone | Name | Key output | Approvals required |
|---|---|---|---|
| **M0** | Workspace Intake & Planning Baseline | This roadmap, threat model, architecture assessment, requirements register | — |
| **M1** | Requirements, Personas & Research | SRS, personas, UX research, competitive analysis, provider licensing, legal review | Owner review |
| **M2** | Architecture, Contracts & Threat Model | ADRs, verdict contract, data model, full threat model, test strategy | Owner review of ADRs |
| **M3** | Secure Foundation & CI | Repo structure, CI/CD, observability, schema, API skeleton, secrets, design system | Owner review of infrastructure choices |
| **M4** | URL Parsing, Lexical Detection & Verdict Core | URL parser, lexical signals, verdict engine, evaluation framework | Security review of SSRF guard |
| **M5** | Threat Intelligence Integration | Licensed TI provider integration, feed ingestion, freshness controls | Legal/license confirmation per provider |
| **M6** | Domain, DNS & TLS Intelligence | Domain signals, DNS analysis, TLS signals, redirect intelligence (passive) | Security review of DNS-touching code |
| **M7** | Web MVP & Browser Extension MVP | Public web app, Chrome extension, warning UX, transparency center | Owner approval; extension store NOT published yet |
| **M8** | Advanced Detection & ML Experiments | ML baseline model, adversarial testing, calibration, model evaluation | Owner approval of ML deployment |
| **M9** | Isolated Deep Scanner | Hardened scanner trust zone, behavioral analysis, independent security review | Owner approval + independent security sign-off required |
| **M10** | Auth, API Productization & Community | User auth, developer API, community reporting, admin workflows | Owner approval |
| **M11** | Enterprise Capabilities | Multi-tenant, policy engine, integrations, enterprise auth | Owner approval + customer demand validation |
| **M12** | Production Hardening & Controlled Launch | External security assessment, operational drills, production deployment | Owner approval + external security assessor sign-off |

---

## M0 — Workspace Intake and Planning Baseline

**Status:** IN PROGRESS (this document is the output)

### Objective
Establish verified workspace state, audited knowledge base, initial requirements register, architecture assessment, threat model, detection strategy, and dependency-aware roadmap.

### Scope
- Read all project instructions and docs
- Verify repository state (code, tests, git history, tools)
- Audit 103 blueprint sections with dispositions
- Create initial requirements register
- Produce architecture assessment (M0 hypothesis)
- Produce initial threat model
- Produce detection strategy
- Produce this roadmap
- Update project state files

### Deliverables
- [x] `records/architecture/M0-WORKSPACE-AUDIT-2026-11-03.md`
- [x] `plans/M0-BLUEPRINT-INTAKE-AND-REQUIREMENTS.md`
- [x] `records/architecture/M0-ARCHITECTURE-ASSESSMENT-2026-11-03.md`
- [x] `records/security/M0-THREAT-MODEL-2026-11-03.md`
- [x] `records/product/M0-DETECTION-STRATEGY-2026-11-03.md`
- [x] `plans/M0-IMPLEMENTATION-ROADMAP.md` (this file)
- [ ] Updated project-state files (in progress)
- [ ] Quality/verification strategy
- [ ] UX/product quality strategy
- [ ] Delivery/operations strategy

### Acceptance criteria
- All 103 blueprint sections have documented dispositions ✓
- Workspace verified from Git log and file listing ✓
- No application code falsely claimed to exist ✓
- Threat model covers all mandatory areas from `THREAT_MODEL_SEED.md` ✓
- Architecture recommendation has documented reasoning ✓
- Security risks and trust boundaries identified ✓
- Detection limitations and UNKNOWN states documented ✓
- Roadmap has explicit dependencies ✓

---

## M1 — Requirements, Personas and Research

**Status:** NOT STARTED  
**Depends on:** M0 complete

### Objective
Produce verified, prioritized, traceable requirements; validated personas and user journeys; competitor analysis; provider licensing assessment; legal/privacy research; and measurable non-functional requirements.

### Scope
- Formal Software Requirements Specification (SRS)
- Validated personas (at minimum: casual consumer, security-aware user, developer, enterprise admin)
- User journey maps for: URL scan flow, warning UX, false-positive reporting, extension install
- Abuse/misuse cases for all major flows
- Competitor analysis: Google Web Risk, VirusTotal, urlscan.io, Netcraft, PhishTank, SmartScreen
- Provider licensing review: Web Risk, URLhaus, PhishTank, OpenPhish (commercial terms)
- Legal/privacy research: India DPDPA, GDPR applicability, CCPA
- Non-functional requirements: latency budgets, availability targets, error budgets, accessibility targets
- UX research: competitive UX analysis, design direction selection (with rationale)

### Explicit exclusions
- No application code
- No design implementation (only direction choice + rationale)
- No provider integration (only licensing research)

### Security considerations
- Privacy impact assessment for each data type collected
- Abuse case documentation for URL submission, reporting, and community features
- Extension permissions justification document

### Required tests
- None in M1 (planning phase); test strategy updated

### Acceptance criteria
- SRS contains functional requirements for all ACCEPT-MVP blueprint sections
- Every requirement has: ID, description, priority, source, acceptance criteria, security/privacy implications
- Provider licensing status documented with source URLs and access dates
- Legal review completed or formally deferred with documented blocker
- UX research report exists with competitor teardowns and design direction decision
- Non-functional requirements are measurable (numbers, not adjectives)

### Risks
- Provider licensing may block certain integrations (e.g., PhishTank commercial terms unclear)
- Legal review may require external counsel for DPDPA compliance
- Competitor research may reveal critical gaps or prior art

### Required human approvals
- Owner review and approval of product scope before M2
- Owner decision on blockchain (section 023) — conventional tamper-evident log vs blockchain
- Owner decision on initial deployment target (provider choice for ADR-003)

### Next eligible milestone after completion
- M2 (Architecture, Contracts & Threat Model)

---

## M2 — Architecture, Contracts and Threat Model

**Status:** NOT STARTED  
**Depends on:** M1 complete; provider licensing clarified; owner scope decisions received

### Objective
Produce locked architecture ADRs, canonical verdict contract, data model, full component-level threat model, test strategy, and deployment design. All major irreversible technical decisions made and documented here.

### Scope
- ADR-001 (backend language/framework)
- ADR-002 (frontend framework)
- ADR-003 (deployment target)
- ADR-004 (verdict schema — labels, versioning, signing strategy)
- ADR-005 (TI provider selection)
- ADR-006 (scanner isolation technology — for future M9)
- ADR-007 (auth provider — for future M10)
- ADR-008 (blockchain vs conventional tamper-evident log)
- System context diagram (C4 Level 1 and Level 2)
- Data flow diagrams for: URL submission, TI ingestion, extension lookup, verdict caching
- Trust zone diagram
- Full STRIDE threat model per component (expanding M0 seed)
- Data model (PostgreSQL schema, Redis structures, object storage structure)
- Verdict contract specification (JSON schema, versioning, signing)
- Test strategy (requirements-to-test traceability matrix)
- Performance budgets (API latency, extension overhead, web vitals)
- Deployment design (environment separation, IaC technology, secret management)
- CI/CD pipeline design (stages, gates, required checks)

### Security considerations
- SSRF protection subsystem design (must be complete before M3 implementation)
- Scanner isolation design (must be complete — reviewed and approved — before M9)
- Secret management architecture
- Key separation design
- Service identity model

### Required human approvals
- Owner approval of all ADRs (especially deployment target, verdict contract, blockchain decision)
- Independent security review of SSRF protection design and scanner isolation design

### Acceptance criteria
- All 8 ADRs exist with alternatives, tradeoffs, decision, and rationale
- Verdict contract is JSON-schema validated
- Trust zones and data flows are diagrammed
- SSRF protection design covers all IP/scheme/redirect attack vectors
- Test strategy has requirements-to-test traceability matrix
- Performance budgets have measurable numbers

---

## M3 — Secure Foundation and CI

**Status:** NOT STARTED  
**Depends on:** M2 ADRs approved; deployment target chosen; tech stack decided

### Objective
Create the development infrastructure, CI/CD pipeline, observability foundation, database schema, API skeleton, secret management, design system tokens, and project scaffolding — all with security-first configuration.

### Scope
- Monorepo/repo structure finalized
- `package.json` / `pyproject.toml` / lockfiles
- Docker dev environment with compose
- PostgreSQL schema (initial, with migrations framework)
- Redis setup and connection pooling
- API skeleton (routes, middleware, error handling, logging)
- OpenTelemetry setup
- CI/CD pipeline (GitHub Actions): lint, type-check, unit tests, SAST, dependency scan, secret scan, build
- Secret management setup (no secrets in repo)
- Design system: color tokens, typography, spacing, semantic verdict tokens
- `.gitignore`, `.env.example`, `.editorconfig`, linting configs
- `CONTRIBUTING.md`, security policy, responsible disclosure placeholder

### Security considerations
- All dependencies pinned with lockfile
- SAST tool configured (Semgrep or Bandit/ESLint-security)
- Secret scanning configured (detect-secrets or gitleaks)
- SCA configured (npm audit / pip-audit / Snyk OSS)
- SSRF guard implementation (the most critical M3 security deliverable)
- No secrets in environment variables committed to repo
- API rate limiting middleware from day one
- Structured logging with URL redaction

### Required tests (must actually run and pass before M3 is complete)
- All existing unit tests pass (initially: empty test suite scaffolding)
- SAST passes with no critical findings
- Secret scanning passes (no detected secrets)
- `docker-compose up` creates working dev environment
- Database migrations run cleanly

### Acceptance criteria (verifiable)
- `git log --oneline` shows at least one commit per major component above
- All CI/CD checks pass on `main` branch (green)
- No secrets in `.git` history (verify with gitleaks)
- SSRF guard has unit tests covering all private IP ranges, IPv6-mapped, metadata endpoints
- API returns structured JSON errors (never stack traces to clients)

---

## M4 — URL Parsing, Lexical Detection and Verdict Core

**Status:** NOT STARTED  
**Depends on:** M3 foundation complete; verdict contract locked (M2); SSRF guard tested (M3)

### Objective
Implement the non-network URL parsing, normalization, lexical analysis, and verdict engine. Establish the evaluation framework with a synthetic test corpus. First version of the detection pipeline (layers 1–4 in detection strategy).

### Scope
- WHATWG-compliant URL parser (using standards-aware library)
- URL normalization: scheme, host, path, query, fragment canonicalization
- IDN/Punycode decoding and confusable detection
- Lexical signals: URL length, entropy, suspicious patterns, encoding, path depth, parameter analysis
- Typosquatting similarity (Levenshtein distance to brand list)
- Scheme validation and allowlisting
- SSRF destination pre-check (reuse M3 guard)
- Verdict engine: multi-signal aggregation → verdict + evidence + confidence
- Evaluation framework: synthetic fixture corpus (labeled, no real malicious content)
- Adversarial URL test corpus (evasion variants: encoded, IDN, IP-literal)
- URL redaction library (remove credentials, tokens from logs)

### Explicit exclusions
- No TI provider calls (M5)
- No DNS resolution (M6)
- No active HTTP requests

### Security considerations
- Fuzzing of URL parser (property-based tests with Hypothesis or similar)
- Adversarial test corpus covers all SSRF bypass variants
- No URL component is logged without redaction

### Required tests (must actually run and pass)
- Unit tests for URL normalization covering WHATWG spec edge cases
- Unit tests for each lexical signal
- Adversarial URL corpus: no known SSRF bypass passes
- Evaluation framework: initial precision/recall baseline measured and recorded
- URL redaction: verified query parameters not appearing in logs

### Acceptance criteria
- URL parser handles WHATWG spec edge cases: trailing dots, IPv6 brackets, IDN, percent-encoding, userinfo
- Lexical signals have documented FP rates on top-1M domain samples
- SSRF guard: 100% of private/reserved/metadata IP tests return BLOCKED (evidence saved)
- Evaluation framework operational: can ingest labeled fixtures and report metrics

---

## M5 — Threat Intelligence Integration

**Status:** NOT STARTED  
**Depends on:** M4 complete; provider licensing verified (M1); provider API keys obtained with owner approval

### Objective
Integrate licensed TI providers, implement feed ingestion, freshness management, source provenance, deduplication, and controlled reputation lookup. Detection layers 1 and 7.

### Scope
- Provider adapter(s) for licensed TI provider(s) (Web Risk + ≥1 other after licensing confirmed)
- Feed ingestion pipeline: pull/push, normalization, deduplication, provenance tracking
- Freshness tracking: per-feed last-updated timestamp; stale-feed behavior = UNKNOWN
- Source confidence weighting
- Redis cache population from feeds
- Verdict integration: TI results feed into verdict engine with evidence provenance
- Provider outage simulation tests: verify UNKNOWN (not BENIGN) on failure

### Security considerations
- Provider credentials in secret manager; never in code or logs
- Response validation: reject malformed/unexpected responses
- Feed delta anomaly detection (sudden mass change = possible poisoning)
- Submitted URLs not sent to providers without policy alignment and disclosure

### Required tests (must actually run and pass)
- Provider outage simulation: mock provider returns error → verdict = UNKNOWN (not BENIGN)
- Stale feed test: feed older than TTL → source marked STALE; not counted as positive evidence
- Integration test with real provider (staging API key): verified lookup returns expected format
- No provider credentials in git (secret scan must pass)

### Required human approvals
- Owner authorization to create provider API accounts and incur any costs
- Confirmation of commercial licensing for each integrated provider

---

## M6 — Domain, DNS and TLS Intelligence

**Status:** NOT STARTED  
**Depends on:** M5 complete; DNS handling reviewed and tested (security gate)

### Objective
Add domain registration signals, DNS record analysis, TLS/certificate intelligence, and passive redirect intelligence. Detection layers 5 and 6.

### Scope
- Controlled DNS resolver (bounded concurrency, timeout, private-range rejection)
- Domain registration signals (where licensed API available)
- DNS records: A, AAAA, CNAME, MX, NS, TXT analysis
- DNS anomaly signals: fast-flux indicators, suspicious NS, short TTL patterns
- TLS certificate analysis: validity, age, issuer, hostname match, CT log presence
- Passive redirect intelligence: analyze redirect chains from cached/submitted data without active fetching
- All DNS answers validated against SSRF guard before any connection

### Security considerations
- DNS rebinding defense: IP pinning per connection
- DNS rebinding tests must pass before M6 is closed
- CNAME chaining must not bypass SSRF guard
- No DNS queries expose user-identifiable information

### Required tests (must actually run and pass)
- DNS rebinding test: short-TTL hostname resolves to public, then private → blocked
- CNAME chain test: CNAME chain resolving to private IP → blocked
- All DNS answers checked against private range allowlist

---

## M7 — Web MVP and Browser Extension MVP

**Status:** NOT STARTED  
**Depends on:** M6 complete; design system established (M3); UX direction approved (M1); verdict contract stable (M2)

### Objective
Deliver a publicly testable (not yet publicly deployed) web application MVP and Chrome extension MVP. Warning UX, transparency center, security education, privacy policy, and responsible disclosure policy.

### Scope
- **Web app:** Home page (URL scanner), scan result page (full evidence display), transparency center, security education, privacy policy, terms of service, responsible disclosure
- **Extension:** Chrome MV3 with real-time navigation protection, local cache, warning interstitial (full-page), popup dashboard, false-positive reporting, protection toggle
- **Warning UX:** Plain-language explanations; deliberate override for MALICIOUS; UNKNOWN state clearly communicated; HTTPS ≠ Safe messaging
- **Performance:** LCP ≤ 2.5s, INP < 200ms, CLS < 0.1 at P75 (measured)
- **Accessibility:** WCAG 2.2 AA target; keyboard navigation; screen reader testing; color + text indicators
- **Responsive:** Mobile (320px), tablet, laptop, desktop, wide (1920px)
- **SEO:** Technical SEO (meta tags, canonical, sitemap); scan result pages NOT indexed by default (noindex)

### Explicit exclusions
- User authentication / accounts (M10)
- Community reporting (M10)
- Deep scanner (M9)
- ML models (M8)
- Developer API (M10)
- Extension publishing to Chrome Web Store (requires owner approval — not in M7)

### Security considerations
- Extension CSP: `script-src 'self'`; no eval; no remote code
- Extension permissions: minimum required (declarativeNetRequest, webNavigation, storage, activeTab)
- No browsing history collection
- Rate limiting on web scan endpoint
- Result pages: noindex meta tag; no full URL in page title or og:url

### Required tests (must actually run and pass)
- Cross-browser: Chrome (primary), Edge, Firefox (basic)
- Responsive viewport tests: 320px, 768px, 1280px, 1920px
- Accessibility: axe-core automated + manual screen reader spot-check
- Performance: Lighthouse CI score ≥ 80 (measured, not claimed)
- Extension: load in Chrome without errors; navigation interception works; false-positive report flow works
- Warning UX: user study or usability review (even informal) before claiming comprehensibility

### Required human approvals
- Owner review and approval of public-facing copy (especially verdict language and safety messaging)
- Owner approval before any extension is submitted to Chrome Web Store

---

## M8 — Advanced Detection and ML Experiments

**Status:** NOT STARTED  
**Depends on:** M7 complete; labeled dataset obtained; MLOps infrastructure; evaluation framework mature (M4)

### Objective
Train, evaluate, and deploy a baseline ML model for URL classification. Implement calibration. Measure impact vs rules-only baseline. Must not introduce new false positives without documented tradeoff.

### Required pre-conditions (must all be verified before starting ML)
- Licensed labeled dataset (documented source, license, size)
- Domain-grouped train/test split implemented
- Time-based evaluation implemented
- Rules-only baseline metrics recorded
- MLOps pipeline operational (reproducible training, versioning, registry)

### Required human approvals
- Owner approval of ML model deployment to production

---

## M9 — Isolated Deep Scanner

**Status:** NOT STARTED  
**Depends on:** M8 complete (detection stable); full scanner trust-zone design (M2); **independent security review of scanner design** (required gate — cannot be bypassed)

### Pre-conditions (all required — no exceptions)
- Full threat model and trust-zone diagram for scanner reviewed and approved
- Scanner isolation technology selected (ADR-006) and verified
- Default-deny egress enforced at network level (not just application code)
- No production credentials or secrets in scanner environment
- Kill switch implemented and tested
- Automated teardown after every scan verified
- Redirect-by-redirect IP validation tested
- DNS rebinding defense in scanner verified
- Resource limits (CPU, RAM, time, response size) tested and enforced

### Required human approvals
- Owner approval
- **Independent security sign-off** (external or second internal reviewer not involved in scanner implementation)

---

## M10 — Auth, API Productization and Community

**Status:** NOT STARTED  
**Depends on:** M7 complete and stable; API contract stable; abuse model documented

### Scope
- User authentication (email/OAuth/passkeys/MFA)
- Session management and account recovery
- User scan history with privacy controls and deletion
- Developer API: keys, quotas, rate limits, versioning, OpenAPI docs
- Community false-positive reporting with moderation
- Admin control plane (separate, strongly authenticated)
- Security audit trail (admin/verdict/key operations)

---

## M11 — Enterprise Capabilities

**Status:** NOT STARTED  
**Depends on:** M10 complete; validated enterprise customer demand; multi-tenant isolation design complete and reviewed

### Scope (only after demand validated)
- Organization accounts and admin console
- Enterprise SSO (OIDC/SAML)
- RBAC and fine-grained permissions
- Tenant isolation (row-level security + audit)
- Enterprise policy engine
- Webhook system
- SIEM integration (basic)

---

## M12 — Production Hardening and Controlled Launch

**Status:** NOT STARTED  
**Depends on:** All prior milestones complete; external security assessment; operational readiness review

### Required before launch (non-negotiable)
- External security assessment (penetration testing by qualified third party)
- Operational drills: incident response, backup/restore, scanner kill switch, key rotation
- All critical/high security findings resolved with evidence
- Monitoring and alerting live and tested
- Rollback procedures tested
- Owner approval for production deployment
- Owner approval for extension publishing
- No fabricated metrics, testimonials, or capabilities in any public-facing content

---

## Dependency graph (simplified)

```
M0 → M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8 → M9 → M10 → M11 → M12
              ↓
         (ADRs gate M3)
                        ↓
                 (Provider licensing gates M5)
                                              ↓
                                    (Security gate gates M9)
                                                           ↓
                                                  (Demand gates M11)
```

---

## Research questions pending resolution

| Question | Blocks | Action |
|---|---|---|
| PhishTank commercial licensing terms | M5 | Legal review in M1 |
| URLhaus commercial terms | M5 | Legal review in M1 |
| India DPDPA applicability and requirements | M7 (launch) | Legal counsel in M1 |
| Firecracker vs gVisor vs cloud sandbox for scanner | M9 | Research + ADR-006 in M2 |
| Blockchain vs tamper-evident log — owner decision | M10+ | Owner decision (see ADR-008) |
| Deployment target (cloud provider) | M3 | Owner decision (see ADR-003) |
| Backend language (Python vs TypeScript) | M3 | ADR-001 in M2 |

