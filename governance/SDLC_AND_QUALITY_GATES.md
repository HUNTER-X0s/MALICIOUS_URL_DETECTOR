# Seven-Stage SDLC and Mandatory Quality Gates

Security, privacy, accessibility, performance and operations run through every stage.

## 1. Planning and feasibility
Problem, customer, scope, success metric, business model hypothesis, provider cost, feasibility, legal exposure, threat environment, dependencies and alternatives. Gate: evidence-backed problem and proceed decision.

## 2. Requirements analysis
Functional/non-functional requirements, user journeys, abuse cases, privacy, accessibility, browser scope, testable acceptance and traceability. Gate: prioritized testable requirements and out-of-scope list.

## 3. System design
System context, trust boundaries, data flows, contracts, verdict schema, threat model, data model, UX, observability, failure modes and rollout. Record ADRs. Gate: critical risks mitigated; scanner trust zone designed before active scanning.

## 4. Development
Small vertical slices, secure defaults, code review, static analysis, schema checks, unit/component tests and docs. Gate: no unreviewed critical/high issue, tests pass, changes reviewable.

## 5. Testing and QA
Unit, component, integration, contract, API, E2E, regression, smoke, cross-browser/extension, accessibility, visual, performance, load, stress, soak, resilience, privacy, fuzz/property-based, security and adversarial tests as applicable. Gate: evidence saved and residual risks accepted by authorized owner.

## 6. Deployment and release
Reproducible artifacts, provenance/SBOM, staging, smoke/DAST/canary, monitoring and rollback. Gate: production only with explicit authorization, release checklist, rollback and operational readiness.

## 7. Maintenance and operations
SLOs, latency/errors, provider health/freshness, queue age, model drift, security, cost, support, patching, incident response, backup restore and postmortems. Gate: owned corrective actions and regression tests.

## Global release blockers
- Critical/high exploitable issue without approved mitigation.
- Scanner can reach private/loopback/link-local/metadata targets.
- Untrusted content executes outside scanner isolation.
- Authz or tenant isolation unverified.
- Sensitive URLs/secrets leak through logs/telemetry/providers.
- SAFE produced only because feeds failed or were empty.
- Tests claimed as passing without evidence.
- No rollback, monitoring or recovery for material release.
- Material accessibility defects or misleading safety messages.
