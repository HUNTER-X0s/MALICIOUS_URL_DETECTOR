# Backlog

**Updated:** 2026-11-03 (M0-INIT)  
**Format:** ID | Description | Milestone | Priority | Notes

---

## M1 Backlog (Requirements and Research)

| ID | Item | Priority | Notes |
|---|---|---|---|
| M1-001 | Software Requirements Specification (SRS) | CRITICAL | All ACCEPT-MVP blueprint sections; functional + non-functional requirements |
| M1-002 | Validated personas and JTBD | CRITICAL | Consumer, security-aware, developer, enterprise admin; accessibility needs |
| M1-003 | User journey maps | HIGH | URL scan, warning interstitial, false-positive report, extension install |
| M1-004 | Abuse and misuse case documentation | HIGH | URL bombing, SSRF attempts, report abuse, scraping |
| M1-005 | Competitor UX teardowns | HIGH | VirusTotal, urlscan.io, Netcraft, Web Risk, Cisco Talos |
| M1-006 | Provider licensing legal review | CRITICAL | PhishTank, URLhaus, OpenPhish, Web Risk commercial terms |
| M1-007 | Privacy/legal research | HIGH | India DPDPA, GDPR applicability, CCPA if needed |
| M1-008 | UX research and design direction decision | HIGH | Evaluate minimalism, editorial, trust-centred approaches |
| M1-009 | Non-functional requirements with measurable targets | HIGH | API latency P95, availability SLA, error budget, Web Vitals |
| M1-010 | Extension permissions justification document | HIGH | Chrome/Edge/Firefox minimum permissions analysis |
| M1-011 | Responsible disclosure policy draft | MEDIUM | Even minimal version before any public exposure |

## M2 Backlog (Architecture and Contracts)

| ID | Item | Priority | Notes |
|---|---|---|---|
| M2-001 | ADR-001: Backend language/framework | CRITICAL | Python/FastAPI vs TypeScript/Node; after owner decision |
| M2-002 | ADR-002: Frontend framework | HIGH | Next.js vs SvelteKit |
| M2-003 | ADR-003: Deployment target | CRITICAL | After owner decision |
| M2-004 | ADR-004: Verdict schema | CRITICAL | Labels, versioning, signing strategy; JSON schema |
| M2-005 | ADR-005: TI provider selection | HIGH | After licensing confirmed |
| M2-006 | ADR-006: Scanner isolation technology | HIGH | Firecracker vs gVisor vs cloud sandbox |
| M2-007 | ADR-007: Auth provider | MEDIUM | For M10; research now |
| M2-008 | ADR-008: Blockchain vs tamper-evident log | MEDIUM | After owner decision |
| M2-009 | Full STRIDE threat model per component | CRITICAL | Expand M0 seed |
| M2-010 | C4 system context and container diagrams | HIGH | Level 1 and Level 2 |
| M2-011 | SSRF protection design specification | CRITICAL | All vectors; reviewed before M3 implementation |
| M2-012 | Scanner trust-zone design | HIGH | For M9; must be complete and reviewed before M9 starts |
| M2-013 | Data model (PostgreSQL schema) | HIGH | Initial schema with privacy annotations |
| M2-014 | Test strategy and requirements-to-test matrix | HIGH | Full portfolio |
| M2-015 | Performance budget specification | HIGH | Measurable targets per component |

## M3 Backlog (Secure Foundation)

| ID | Item | Priority | Notes |
|---|---|---|---|
| M3-001 | Repo structure and monorepo setup | CRITICAL | apps/, services/, packages/, tests/ |
| M3-002 | Package.json / pyproject.toml / lockfiles | CRITICAL | Depending on ADR-001 decision |
| M3-003 | Docker Compose dev environment | HIGH | Database, Redis, API, worker |
| M3-004 | PostgreSQL schema and migrations framework | CRITICAL | |
| M3-005 | Redis setup | HIGH | Connection pooling, namespacing |
| M3-006 | API skeleton | HIGH | Routes, middleware, error handling |
| M3-007 | SSRF guard implementation | CRITICAL | Must pass all test vectors before M4 |
| M3-008 | URL redaction library | CRITICAL | Remove credentials/tokens from logs |
| M3-009 | Structured logging setup | CRITICAL | No raw URLs in logs |
| M3-010 | OpenTelemetry integration | HIGH | Metrics, traces, logs |
| M3-011 | GitHub Actions CI | CRITICAL | Lint, type-check, unit tests, SAST, secret scan, SCA |
| M3-012 | Secret management setup | CRITICAL | No secrets in repo |
| M3-013 | Design system tokens | MEDIUM | Color, typography, spacing, verdict state tokens |
| M3-014 | Rate limiting middleware | HIGH | Per-IP and per-key |
| M3-015 | CONTRIBUTING.md, security policy | MEDIUM | Before any public exposure |

## Research questions backlog

| ID | Question | Blocks | Status |
|---|---|---|---|
| RQ-001 | PhishTank commercial API licensing terms | M5 | OPEN |
| RQ-002 | URLhaus commercial terms and feed licensing | M5 | OPEN |
| RQ-003 | OpenPhish API terms and pricing | M5 | OPEN |
| RQ-004 | Google Web Risk pricing and quota | M5 | OPEN — documented as commercial API |
| RQ-005 | India DPDPA compliance requirements | M7 launch | OPEN |
| RQ-006 | Firecracker (AWS microVM) usability on chosen cloud | M9 | OPEN |
| RQ-007 | gVisor (Google Cloud) scanner isolation capability | M9 | OPEN |
| RQ-008 | WHOIS/RDAP licensing for domain age signals | M6 | OPEN |
| RQ-009 | Passive DNS provider options and licensing | M6 | OPEN |
| RQ-010 | Chrome Web Store submission requirements and review time | M7+ | OPEN |

## Deferred/Future backlog (not in initial scope)

- Email security expansion (§041)
- QR security (§042)
- Download protection (§043)
- Mobile security (§044)
- AI assistant / RAG (§094–097)
- Government-grade features (§037)
- Threat graph (§027)
- Threat campaign detection (§028)
- SIEM/SOC integrations (§070)
- Gamification (§090)
- CLI (§086)
