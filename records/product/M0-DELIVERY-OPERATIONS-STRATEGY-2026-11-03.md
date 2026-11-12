# URLSentinel — Delivery and Operations Strategy (M0)

**Date:** 2026-11-03  
**Reference:** `docs/09-operations/CICD_AND_RELEASE.md`, `docs/09-operations/RELIABILITY_AND_SRE.md`, `docs/09-operations/SLO_OBSERVABILITY_AND_COST.md`, `governance/SDLC_AND_QUALITY_GATES.md`

---

## 1. Local development

**Requirements:**
- Docker Compose for local dev: API, PostgreSQL, Redis, optional worker
- `.env.example` template with placeholder values (no real secrets)
- `make` or npm/pnpm scripts for common tasks: start, test, lint, migrate, build
- First-time setup should work in < 15 minutes on a clean machine
- Database migrations: automated on start; rollback script required for every migration

**Local security:**
- No production secrets in `.env` files
- Local JWT signing uses dev-only keys (never shared)
- Local dev does not connect to production databases or live providers

---

## 2. Reproducible environments

| Environment | Purpose | Differences from prod |
|---|---|---|
| `dev` (local) | Developer workstation | Hot reload; debug logging; mock providers; dev secrets |
| `staging` | Integration and QA | Full cloud infrastructure; real (test) provider keys; DAST possible here; owner-approved deployments |
| `prod` | Live product | Production credentials; monitoring; CDN; WAF; owner-approved only |

**Environment parity:**
- All three environments use the same container images (different configs only)
- Infrastructure-as-code from M3; all environments defined in code
- No manual configuration of production resources (everything is code-reviewed)

---

## 3. Configuration and secrets management

**Principles:**
- Secrets never in: source code, `.env` files in staging/prod, CI environment variables that are logged, issue tracker, Slack, chat
- Dev: local `.env` (not committed); documented in `.env.example`
- Staging/prod: cloud-native secret manager (chosen with deployment target in ADR-003)
- Rotation: automated rotation for database credentials; documented rotation runbooks for API keys
- Audit: every secret access logged in secret manager
- Scope: each service receives only the secrets it needs (least privilege)

---

## 4. CI/CD pipeline design

```
Commit / PR
    ↓
Format + Lint + Type check (fail fast, < 2 min)
    ↓
Unit tests + Coverage (< 5 min)
    ↓
SAST (Semgrep/Bandit) — fail on critical
    ↓
Secret scanning (gitleaks) — fail on any detection
    ↓
Dependency scanning (SCA) — fail on critical CVEs
    ↓
Build Docker image
    ↓
Integration tests (< 10 min)
    ↓
─── PR review required ───
    ↓
Staging deployment (on merge to main)
    ↓
Staging smoke tests
    ↓
─── Owner approval required ───
    ↓
Production deployment (manual trigger, approval-gated)
    ↓
Production smoke tests + alerting verification
    ↓
─── Monitor, rollback if needed ───
```

**Pipeline requirements:**
- All CI runs are ephemeral; no persistent state between runs
- Pipeline credentials are scoped to minimum required actions
- Container images are tagged with git commit SHA
- SBOM generated on every build (from M3)
- Deployment artifacts are immutable after build

---

## 5. Staging and production promotion

- Staging: automated on merge to `main`; owner can review before production
- Production: manual trigger; requires owner approval; documented in `records/approvals/`
- Extension: Chrome Web Store submission requires explicit owner review + approval of listing copy
- Production deployment: blue-green or rolling update (chosen in ADR-003); rollback in < 5 minutes
- Database migrations: backward-compatible first; old schema supports new code before new code ships

---

## 6. Monitoring and alerting

**Minimum monitoring from M3:**
| Signal | Alert condition | Severity |
|---|---|---|
| API error rate | > 1% over 5 minutes | HIGH |
| API P99 latency | > 5s over 5 minutes | MEDIUM |
| Queue depth | > 100 items aged > 5 minutes | MEDIUM |
| Threat-feed freshness | Any feed > 24h stale | HIGH |
| Scanner crash rate (M9+) | > 0% | HIGH |
| Secret access anomaly | Unexpected access pattern | CRITICAL |
| Deployment failure | Any step fails | CRITICAL |

**Observability stack:**
- Structured JSON logs → log aggregator (cloud-native)
- Metrics → Prometheus-compatible collection
- Traces → OpenTelemetry → distributed trace backend
- Alerts → PagerDuty / email / Slack (TBD by ADR-003)
- Dashboard: key metrics visible at a glance

**Privacy in observability:**
- Never log: raw submitted URLs, query parameters, user credentials, API keys, provider responses (raw)
- Log only: hashed URL identifiers, verdict outcomes, latency, error codes, signal counts

---

## 7. Backups and recovery

| Data | Backup frequency | Retention | Recovery objective |
|---|---|---|---|
| PostgreSQL (primary) | Continuous WAL + daily snapshot | 30 days | RPO: < 1 hour; RTO: < 4 hours |
| PostgreSQL (audit log) | Daily snapshot | 2 years | RPO: < 24 hours; RTO: < 8 hours |
| Redis (cache) | Not backed up — ephemeral cache | N/A | Recovery: rebuild from DB/feeds |
| Object storage | Versioned with cloud provider | Per-type retention | Depends on object type |
| Infrastructure-as-code | Git (always) | Forever | Redeploy from code |
| Secrets | Cloud secret manager versioning | Managed by provider | Audit trail maintained |

**Recovery requirements:**
- Backup restore tested before production launch (M12)
- DR runbook documented and tested with timed drill
- RTO/RPO targets confirmed feasible with chosen cloud provider

---

## 8. Incident response

**Severity levels:**
| Level | Definition | Response time | Examples |
|---|---|---|---|
| P1 — Critical | Product unavailable or actively harming users | < 15 minutes | SSRF exploited, scanner escape, verdict integrity breach |
| P2 — High | Major feature degraded, security event | < 1 hour | Feed down > 2h, extension blocking good URLs at scale |
| P3 — Medium | Minor degradation, no immediate user harm | < 4 hours | Elevated error rate, latency spike |
| P4 — Low | Cosmetic or future-risk issue | Next business day | Visual bug, low-priority FP |

**Incident response playbooks needed (before M12):**
- Compromised signing key
- Scanner escape to production
- Database breach (URL/verdict data)
- Extension malicious update (supply chain)
- SSRF exploitation
- TI provider feed poisoning
- API key compromise

**Playbook format:** `records/incidents/TEMPLATE_POSTMORTEM.md`

---

## 9. Rollback

- Application: redeploy previous container image (< 5 minutes)
- Database: migration rollback script required for every migration before it ships
- Extension: Chrome Web Store allows rollback to previous version; have a process documented
- Feature flags: where practical, use feature flags to disable features without full rollback
- Scanner (M9+): fleet kill switch kills all running scanner jobs and stops new submissions

---

## 10. Dependency management

- All dependencies pinned to exact versions with lockfile (package-lock.json / poetry.lock)
- Weekly automated dependency updates (Dependabot-style) — reviewed, tested, merged deliberately
- SCA alert on new critical CVE: emergency patch within 48 hours with evidence
- No direct import of unreviewed packages
- Extension dependencies: extra scrutiny; each added dependency extends attack surface

---

## 11. Release readiness checklist (before M12 launch)

Documented in `records/releases/TEMPLATE_RELEASE_CHECKLIST.md`. Key items:
- [ ] External security assessment completed with findings resolved
- [ ] All critical and high security findings resolved (with evidence)
- [ ] Performance targets met and measured
- [ ] Accessibility requirements met (automated + manual evidence)
- [ ] Privacy policy and terms of service live
- [ ] Responsible disclosure policy live
- [ ] Monitoring and alerting live and tested
- [ ] Backup restore tested within last 30 days
- [ ] Incident response playbooks documented and reviewed
- [ ] Owner approval documented in `records/approvals/`
- [ ] No fabricated metrics, testimonials, or unverified capability claims in any public content
- [ ] Extension listing reviewed and approved by owner before submission

---

## 12. Production deployment authorization

Production deployment and extension publishing are **owner-approval-gated**.

Before any production deployment:
1. Owner reviews deployment scope and evidence
2. Deployment plan documented with rollback procedure
3. Owner provides explicit written approval (recorded in `records/approvals/`)
4. Deployment proceeds with owner availability for rollback decision if needed

