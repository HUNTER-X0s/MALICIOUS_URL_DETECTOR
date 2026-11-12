# URLSentinel — Blueprint Intake and Requirements Register (M0)

**Source:** 103-section owner blueprint at `docs/01-product/COMPLETE_PRODUCT_BLUEPRINT_103.md`  
**Traceability base:** `docs/01-product/FEATURE_TRACEABILITY_103.md`  
**Assessment date:** 2026-11-03  
**Assessor:** Antigravity M0-INIT coordination  
**Status:** INITIAL ASSESSMENT — all 103 sections reviewed; dispositions assigned

---

## Interpretation key

| Disposition | Meaning |
|---|---|
| `ACCEPT-MVP` | In scope for Milestone 3–7 (foundation through web/extension MVP) |
| `ACCEPT-DEFER` | Valid requirement; deferred to M8–M12 or beyond |
| `ACCEPT-RESEARCH` | Accepted in principle; needs research gate before implementation |
| `CONSOLIDATE` | Merged into another section for requirements purposes |
| `DEFER-FUTURE` | Valid long-term idea; not in initial product scope |
| `DEFER-GATED` | Requires independent security/privacy gate before consideration |
| `REJECT` | Rejected with rationale; original intent preserved |

---

## Blueprint intake: all 103 sections

| ID | Blueprint section | Disposition | Target milestone | Key rationale / conditions |
|---:|---|---|---|---|
| 001 | Core Product | ACCEPT-MVP | M0–M7+ | Platform identity confirmed. Scope V1: web app + extension + detection core. Enterprise/API/community = later milestones. |
| 002 | Target Users | ACCEPT-MVP | M1 | Personas and JTBD must be formally documented. Priority: consumers, then SMBs, then developers. Children/senior accessibility features in M7. |
| 003 | User-Facing Web Application | ACCEPT-MVP | M3–M7 | Home page + URL scanner + result page = MVP core. Privacy-safe scan history deferred to M10+. |
| 004 | Verdict System | ACCEPT-MVP | M2–M4 | Multi-state verdict system required from M2 contract design. Exact label names require ADR. Risk + confidence separation is mandatory. |
| 005 | Human-Friendly Explanations | ACCEPT-MVP | M4–M7 | Plain-language explanations are a core trust requirement. Must be testable with non-expert users. |
| 006 | Browser Extension | ACCEPT-MVP | M1–M7 | Chrome/Chromium MV3 MVP is in scope for M7. Edge/Firefox separately tested. Minimum permissions mandatory. |
| 007 | Browser Warning System | ACCEPT-MVP | M2–M7 | Full-page warning interstitial with deliberate override required. False-positive escape/report flow required. |
| 008 | Local-First Protection | ACCEPT-MVP | M2–M7 | Cache-first, rules-first, then bounded cloud lookup is an architectural requirement for performance and resilience. |
| 009 | Threat Intelligence Engine | ACCEPT-RESEARCH | M5+ | Provider licensing must be reviewed before production integration. No commercial use of Safe Browsing without Web Risk upgrade. PhishTank, URLhaus terms require verification. |
| 010 | URL Intelligence Engine | ACCEPT-MVP | M4+ | WHATWG URL parsing, IDNA, Unicode, obfuscation patterns are all required before any reputation check. Non-network. |
| 011 | Domain Intelligence | ACCEPT-DEFER | M6+ | WHOIS/passive DNS licensing required. Domain age + registrar signals via licensed providers only. |
| 012 | DNS Security | ACCEPT-MVP | M2, M6+ | DNS rebinding defense must be designed into scanner from M2. DNS record analysis for signals in M6. |
| 013 | TLS / Certificate Intelligence | ACCEPT-MVP | M2, M6+ | TLS signals are useful; HTTPS ≠ Safe rule is a mandatory system invariant documented in M2 contract. |
| 014 | Redirect Intelligence | ACCEPT-DEFER | M6, M9 | Passive redirect analysis (from cached scans) in M6. Active redirect traversal only inside isolated scanner (M9) after security gate. |
| 015 | Brand Protection | ACCEPT-DEFER | M8–M9 | Typosquat/confusable/lookalike signals required; must measure false-positive rate before production deployment. |
| 016 | Content Analysis | DEFER-GATED | M9 | Active HTML/DOM/script analysis only inside isolated scanner. Must pass scanner security gate (M9) before enabling. |
| 017 | Browser-Based Behavioral Analysis | DEFER-GATED | M9 | Playwright/headless in disposable VM only, after M9 security gate. |
| 018 | Isolated Scanner | DEFER-GATED | M9 | Requires full trust-zone design (M2), independent security review, and explicit owner approval before any hostile content execution. |
| 019 | SSRF Protection | ACCEPT-MVP | M0–M3, M6, M9 | Non-negotiable. SSRF subsystem must be designed before any network-touching feature. Dedicated threat model required. |
| 020 | Security Boundary Architecture | ACCEPT-MVP | M2–M3 | Trust-zone diagram, data flows, service identities, egress model required in M2. |
| 021 | Cryptographically Signed Verdicts | ACCEPT-DEFER | M10+ | Major trust feature but requires stable verdict schema first. Key rotation/revocation design required. |
| 022 | Tamper-Evident Evidence | ACCEPT-DEFER | M10+ | Evidence hashing and audit trail architecture deferred until verdict schema and evidence model are stable (M4+). |
| 023 | Blockchain Layer | ACCEPT-RESEARCH | Research first | Blockchain only if multi-party provenance need is validated and cost/governance/privacy tradeoffs are acceptable. Current assessment: premature. Needs explicit research gate and owner decision. |
| 024 | AI / ML Layer | ACCEPT-DEFER | M8+ | ML only after: licensed training data, baseline rules established, leakage-safe evaluation methodology, operational plan. |
| 025 | ML Security | ACCEPT-DEFER | M8+ | Poisoning, adversarial evasion, contamination controls required when ML is introduced. |
| 026 | MLOps | ACCEPT-DEFER | M8+ | Reproducible pipeline only when models are production-approved. |
| 027 | Threat Graph | DEFER-FUTURE | M11+ | Campaign-level detection is a long-term capability. Requires stable entity identifiers, data quality, and scale. |
| 028 | Threat Campaign Detection | DEFER-FUTURE | M11+ | Depends on threat graph. Future capability. |
| 029 | Community Threat Intelligence | ACCEPT-DEFER | M10+ | Community reporting requires abuse-resistant system, moderation, verification, and identity model. Not in MVP. |
| 030 | Reporter Reputation | ACCEPT-DEFER | M10+ | Depends on community reporting infrastructure. |
| 031 | Analyst Platform | ACCEPT-DEFER | M10+ | Internal analyst dashboard for false-positive triage, model oversight. After public product is live. |
| 032 | Security Researcher Portal | DEFER-FUTURE | M10+ | Verified researcher program requires operational readiness and legal framework. |
| 033 | Privacy Architecture | ACCEPT-MVP | M0–M12 | Cross-cutting. Data minimization, redaction, retention/deletion, transparency are mandatory from day one. |
| 034 | Authentication | ACCEPT-DEFER | M7, M10+ | Anonymous scan is the MVP. Auth only when account-linked features (history, settings) are implemented. Strong MFA from the start when auth is added. |
| 035 | Authorization | ACCEPT-MVP | M2–M12 | RBAC/service identities are required at M3 even before user accounts, for internal service boundaries. |
| 036 | Enterprise Security | DEFER-FUTURE | M11+ | Organization accounts, admin console, policy engine after customer validation. |
| 037 | Government-Grade Features | DEFER-FUTURE | M11+ | Government procurement requires jurisdiction-specific research. Not in initial scope. |
| 038 | Developer Platform | ACCEPT-DEFER | M10+ | Public API with keys/quotas/docs after internal API stabilizes. |
| 039 | Webhook System | ACCEPT-DEFER | M10+ | After developer platform. Requires signed/idempotent delivery. |
| 040 | Integrations | DEFER-FUTURE | M11+ | SIEM/SOAR/EDR/Slack/Teams integrations deferred to enterprise tier. |
| 041 | Email Security Expansion | DEFER-FUTURE | Separate track | Gmail/Outlook integration requires separate product track, privacy review, and email API authorization. |
| 042 | QR Security | DEFER-FUTURE | Separate track | QR phishing is a real threat but requires separate mobile/camera UX track and privacy review. |
| 043 | Download Protection | DEFER-FUTURE | Separate track | File analysis requires a separate malware-analysis trust boundary. Out of initial scope. |
| 044 | Mobile Security | DEFER-FUTURE | Separate track | iOS/Android native requires separate OS-specific capabilities and separate product track. |
| 045 | UX Personalization | ACCEPT-MVP | M1–M7 | Dark/light mode, simple/advanced view, keyboard navigation, accessibility preferences in MVP. |
| 046 | Accessibility | ACCEPT-MVP | M1–M12 | WCAG 2.2 targeted compliance is mandatory. Color-plus-text indicators, screen reader support, keyboard navigation required. |
| 047 | Internationalization | ACCEPT-DEFER | M7+ | i18n architecture in M7 (en default). Hindi and other languages only after qualified translation and regional threat intelligence. |
| 048 | Performance Engineering | ACCEPT-MVP | M2–M12 | Performance budgets defined in M2. CDN, edge caching, Redis, code splitting in MVP. LCP ≤2.5s, INP <200ms, CLS <0.1 targets at P75. |
| 049 | Low-Latency Detection | ACCEPT-MVP | M2–M12 | Local-first cache + bloom filter + fast API path. Target: P95 API response <500ms for cached lookups. Deep path async. |
| 050 | Data Structures & Algorithms | ACCEPT-MVP | M2, M4–M8 | Appropriate CS primitives (hash lookups, bloom filters, tries) only where benchmarks show meaningful benefit. |
| 051 | Caching Architecture | ACCEPT-MVP | M2, M5–M7 | Multi-layer cache (extension → CDN → Redis → DB) with freshness, privacy, invalidation controls. |
| 052 | Bloom Filter / Probabilistic Threat Lookup | ACCEPT-DEFER | M4+ | Bloom filter for extension's "fast miss" path. Only after measured scale/space benefit and acceptable FP handling. |
| 053 | Distributed Systems | ACCEPT-DEFER | M2–M12 | Stateless services, message queues, worker pools where justified. Start with modular monolith. No premature microservices. |
| 054 | Fault Tolerance | ACCEPT-MVP | M3–M12 | Graceful degradation required. Feed down, ML down, scanner down must not produce SAFE verdicts. |
| 055 | Resilience Engineering | ACCEPT-MVP | M2–M12 | Timeouts, bounded retries, backpressure, DLQ, idempotency, recovery tests required from M3. |
| 056 | DDoS Protection | ACCEPT-MVP | M3, M12 | CDN/WAF/rate limiting from the start. Full stress testing in M12 before launch. |
| 057 | Abuse Prevention | ACCEPT-MVP | M0–M12 | Rate limiting, bot detection, queue protection, cloud-bill abuse prevention required from M3. |
| 058 | Secret Management | ACCEPT-MVP | M3–M12 | Managed secret storage, no secrets in git/browser/logs/prompts. Short-lived credentials. |
| 059 | Key Security | ACCEPT-MVP | M2, M10+ | Cryptographic key separation and KMS evaluation required in M2 design. HSM evaluation for signing keys. |
| 060 | Zero Trust Architecture | ACCEPT-MVP | M0–M12 | Service identity, explicit authorization, least privilege at every boundary. Not just the network perimeter. |
| 061 | Supply-Chain Security | ACCEPT-MVP | M3–M12 | Dependency/SBOM/SCA, secret scanning, container scanning, signed artifacts in M3 CI setup. |
| 062 | Secure CI/CD | ACCEPT-MVP | M3–M12 | Protected branches, automated security gates, staged promotion, rollback from M3. |
| 063 | Testing | ACCEPT-MVP | M1–M12 | Risk-based test strategy required. Full portfolio per `docs/08-quality/TEST_STRATEGY.md`. |
| 064 | Security Testing | ACCEPT-MVP | M0–M12 | SSRF, XSS, injection, auth bypass, IDOR, extension, scanner tests. Only authorized targets. |
| 065 | Fuzzing | ACCEPT-DEFER | M4–M9 | Fuzz URL parser, normalizer, DNS handling, redirect parser, API inputs after they exist (M4+). |
| 066 | Threat Modeling | ACCEPT-MVP | M0–M12 | STRIDE/attack trees/abuse cases for every major component. First full model in M2. |
| 067 | Secure SDLC | ACCEPT-MVP | M0–M12 | Already embedded in governance/SDLC_AND_QUALITY_GATES.md 7-stage model. |
| 068 | Observability | ACCEPT-MVP | M3–M12 | Logs, metrics, traces, alerts from M3. Threat-feed freshness, detection quality, scanner health metrics required. |
| 069 | Security Monitoring | ACCEPT-MVP | M3–M12 | Security event detection, abuse analytics, anomaly alerts from M3. |
| 070 | SIEM/SOC Architecture | DEFER-FUTURE | M11+ | Enterprise SIEM/SOAR integrations only for validated enterprise customers. |
| 071 | Incident Response | ACCEPT-MVP | M3, M12 | Incident playbooks for key/credential/scanner/extension compromise required before M12 launch. |
| 072 | Disaster Recovery | ACCEPT-MVP | M3, M12 | Automated encrypted backups, restore tests, defined RTO/RPO required. |
| 073 | Business Continuity | ACCEPT-DEFER | M11+ | Enterprise SLA continuity planning after enterprise customers acquired. |
| 074 | Threat-Feed Quality Management | ACCEPT-DEFER | M5+ | Source accuracy, freshness, conflict, duplication, FP quality controls when feeds integrated. |
| 075 | Evidence-Based Security | ACCEPT-MVP | M2–M12 | Verdict → signals → evidence → sources → timestamp traceability is a core product invariant. |
| 076 | Security Audit Trail | ACCEPT-MVP | M7, M10+ | Admin, verdict, policy, key operation audit log. Tamper-resistant from M7. |
| 077 | Admin Control Plane | ACCEPT-DEFER | M10+ | Separate, strongly-authenticated admin interface. Not needed before public product has users. |
| 078 | Enterprise Policy Engine | DEFER-FUTURE | M11+ | Tenant policies after enterprise customer validation. |
| 079 | Policy-as-Code | DEFER-FUTURE | M11+ | Versioned policy-as-code after enterprise policy engine. |
| 080 | Multi-Tenant Architecture | DEFER-FUTURE | M11+ | Tenant isolation required before any enterprise offering. Design must be complete before first enterprise customer. |
| 081 | Data Governance | ACCEPT-MVP | M0–M12 | Data classification, retention, deletion, access, residency, ownership from day one. |
| 082 | Compliance Readiness | ACCEPT-RESEARCH | M0 research, M12 | SOC 2/ISO 27001/DPDPA/GDPR research required. Never claim compliance without external audit. |
| 083 | Transparency Center | ACCEPT-MVP | M7+ | Public methodology, privacy, limitations, disclosure, status page in MVP. |
| 084 | Security Research Program | ACCEPT-DEFER | M10+ | Coordinated disclosure policy defined in M7 (minimal). Full program after operational readiness. |
| 085 | Developer Experience | ACCEPT-DEFER | M10+ | OpenAPI docs, SDK samples, self-service console after internal API stabilizes. |
| 086 | CLI | ACCEPT-DEFER | M10+ | CLI after API contract and auth model stable. |
| 087 | Security API for CI/CD | ACCEPT-DEFER | M10+ | CI/CD integration after developer API is stable and safe-fail behavior is defined. |
| 088 | Browser Security Dashboard | ACCEPT-MVP | M7+ | Extension popup status/reporting dashboard. Minimal telemetry. User control. |
| 089 | Personal Security Dashboard | ACCEPT-DEFER | M7+ | Personal scan history with privacy controls. Requires auth (M10+) unless session-local. |
| 090 | Gamification | DEFER-FUTURE | Optional | Security awareness education only. Never gamify risky clicks. Only after user research validates value. |
| 091 | Security Education | ACCEPT-MVP | M7+ | Security education center: phishing guides, safe browsing tips, scam awareness. In MVP. |
| 092 | Accessibility for Non-Technical Users | ACCEPT-MVP | M1–M12 | Non-expert understandable plain-language warnings are non-negotiable. Advanced details behind disclosure. |
| 093 | Localization | ACCEPT-DEFER | M7+ | English default. i18n architecture in place. Other languages after qualified review. |
| 094 | AI Assistant | DEFER-FUTURE | Future, gated | Security assistant only with scoped, verified, non-overriding capabilities. Not in initial scope. |
| 095 | RAG Security Assistant | DEFER-FUTURE | Future, gated | RAG only over curated, permissioned, provenance-tracked security sources. Not in initial scope. |
| 096 | AI Safety | ACCEPT-RESEARCH | Before any assistant | AI safety constraints required before any assistant capability is considered. |
| 097 | Threat Intelligence RAG | DEFER-FUTURE | Future, gated | TI-RAG with source citations after data quality and access-control model established. |
| 098 | Human-in-the-Loop Security | ACCEPT-DEFER | M8, M10+ | Analyst review queue for ambiguous/high-impact cases. Requires analyst platform (M10+). |
| 099 | Security Confidence Calibration | ACCEPT-MVP | M2, M4, M8 | UNKNOWN/UNDER_REVIEW as first-class outcomes is a non-negotiable invariant. Explicit in M2 verdict contract. |
| 100 | Production Engineering Philosophy | ACCEPT-MVP | M0–M12 | Secure by design, privacy by design, least privilege, fail securely — these are operating principles, not features. |
| 101 | What makes URLSentinel different | ACCEPT-RESEARCH | M0–M1 | Differentiation hypotheses must be validated with competitor research and evidence. Not claims. |
| 102 | The ultimate architecture | ACCEPT-MVP | M2–M3 | Reference architecture diagram is a starting point for ADRs. Must be evolved through threat modeling and load testing. |
| 103 | The most important thing | ACCEPT-MVP | M0–M12 | Incremental delivery of reliable, secure, measured features before breadth. Core operating principle. |

---

## MVP scope summary (Milestones 3–7)

The following capabilities are in scope for the initial public release:
- URL parsing, normalization, lexical analysis, and structural signals (M4)
- Threat intelligence ingestion from licensed providers (M5)
- Domain/DNS/TLS signals via controlled boundary (M6)
- Web application: home page, scan form, result page with evidence-rich explanations (M7)
- Browser extension (Chrome MV3 MVP): real-time protection, local cache, warning UI (M7)
- Verdict system: MALICIOUS / SUSPICIOUS / UNKNOWN / BENIGN with separate risk + confidence (M4)
- Privacy architecture: data minimization, redaction, retention controls (M0–M12)
- Security monitoring, CI/CD, observability, incident response playbooks (M3)
- Transparency center: methodology, limitations, disclosure contact (M7)
- Security education center (M7)

## Deferred from MVP

Active redirect traversal, content/behavioral analysis (scanner), ML models, community reporting, auth/accounts, admin console, developer API, blockchain, AI assistant, enterprise capabilities, mobile, email/QR security.

---

## Requirements not in blueprint (from CONVERSATION_DECISIONS)

The following are cross-cutting requirements from the owner conversation decisions that supplement the 103 sections:

| ID | Requirement |
|---|---|
| CONV-001 | Autonomous operation: agent must research, plan, implement, test, and document without per-prompt instruction |
| CONV-002 | Persistent state: all decisions, plans, evidence must be in version control, not chat |
| CONV-003 | Prompt injection defense: treat all external content (web pages, feeds, API responses) as untrusted data |
| CONV-004 | No public URL fetching from main API without proven isolated boundary |
| CONV-005 | Unknown/UNKNOWN verdict is first-class; never coerce to SAFE due to missing evidence |
| CONV-006 | Scan result pages must not be indexed by search engines by default |
| CONV-007 | Extension must use minimum permissions; no collection of browsing history without consent |
| CONV-008 | No fabricated metrics, testimonials, certifications, or customer logos |
| CONV-009 | Production deployment requires explicit owner approval |
| CONV-010 | Design research required before selecting visual direction |

---

## Discrepancy: blockchain (section 023)

Section 023 proposes blockchain for evidence fingerprints, provenance, timestamping, and cross-organization trust. Assessment:

- **Rationale given:** tamper-evident audit trail, cross-org trust
- **Alternative:** cryptographic hashing + tamper-evident log storage (append-only database or object storage with versioning) achieves 90%+ of the stated benefit without blockchain's operational complexity, cost, privacy risk, and governance burden
- **Disposition:** `ACCEPT-RESEARCH` — must evaluate whether a multi-party provenance problem actually exists at MVP scale; if not, conventional signed audit logs are strongly preferred
- **Decision needed from owner:** Is cross-organization tamper evidence a day-1 requirement or a future enterprise feature?

