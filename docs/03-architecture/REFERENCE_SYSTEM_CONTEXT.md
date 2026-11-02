# Reference system context (candidate, not approved architecture)

Potential trust-separated domains:
- Web application and browser extension.
- Public API/auth/rate limiter.
- URL parser and normalization library (no network activity).
- Verdict orchestration and policy engine.
- Reputation/cache adapter layer.
- Domain/DNS/TLS intelligence workers (controlled network egress).
- Deep scan broker and isolated scanner workers (only after dedicated trust zone).
- Threat-feed ingestion and curation.
- Data stores for operational data, audit, caches and research/training artifacts.
- Observability, secrets/key management, admin/analyst capabilities.

Antigravity must produce its own architecture after analysing current requirements, threat model, user scale assumptions, team capability, deployment budget and operational complexity. Do not copy this outline uncritically.
