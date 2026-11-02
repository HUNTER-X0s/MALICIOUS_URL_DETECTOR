# Quality and test strategy

Maintain a requirements-to-test traceability matrix. Include as applicable:
- Static checks: formatting, lint, type checks, schema/API compatibility, complexity.
- Unit and component tests.
- Integration, database and migration tests.
- Contract and API tests (authn/authz, validation, limits, idempotency, errors).
- E2E and critical user journeys.
- Regression and smoke tests.
- Browser/extension cross-browser tests.
- Accessibility tests (automated and manual assistive technology).
- Visual regression and responsive viewport tests.
- Performance, load, stress, soak, capacity and cost tests.
- Security: SAST, DAST, SCA, secret scan, IaC/container scan, fuzz, property-based, SSRF, authz, tenant isolation, CSP/CORS/CSRF, abuse and authorized penetration tests.
- Resilience: dependency outage, rate-limit exhaustion, failover, backup/restore, rollback and disaster recovery.
- Privacy: logging inspection, retention/deletion, data export, consent and network egress.
- ML: temporal validation, leakage, calibration, drift and adversarial evaluation.

Tests must be reproducible and isolated. Save commands, environment, tool versions, date, results, skipped tests, defects and evidence. Do not infer security from coverage percentage alone.
