# Project Governance and Knowledge Management

## Canonical sources
- Product intent: `instructions/PROJECT_DESCRIPTION.md`, `docs/01-product/`.
- Permanent constraints: `instructions/MASTER_PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, `.agents/rules/`.
- Approved architecture: accepted ADRs in `records/decisions/`.
- Current execution: status files and `plans/ROADMAP.md`.
- Evidence: `records/` and linked test/benchmark artifacts.

## Traceability
Use stable IDs such as `PRD-`, `NFR-`, `SEC-`, `UX-`, `PERF-`, `TEST-`, `OPS-`. High-priority requirements map to design, code, verification and release evidence.

## Change control
Changes to verdict semantics, security boundaries, retention, extension permissions, provider sharing, API contracts, auth/tenant model or production infrastructure require an ADR/change record with impact and rollback.

## Documentation hygiene
Never overwrite historical evidence; create dated records. Include author/agent, timestamp, version, scope, sources, confidence and status. Mark obsolete docs and link successors. Review source freshness and contradictions each major milestone.

Statuses: proposed, researching, planned, in_progress, blocked, implemented, verified, released, deprecated. Status is evidence-backed.
