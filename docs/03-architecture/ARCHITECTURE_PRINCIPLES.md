# Architecture principles

1. Start with a modular monolith/API and explicit domain boundaries unless measurable requirements justify distributed services.
2. Separate public request handling from active network scanning. The primary API should parse and orchestrate, not fetch arbitrary user-supplied URLs.
3. Isolate components by trust level and privilege. Keep scanner, feed ingest, ML training and public API distinct where their risk profiles differ.
4. Define canonical, versioned contracts for verdicts, evidence, source provenance, scan jobs and APIs.
5. Use explicit timeouts, bounded concurrency, circuit breakers, backpressure, idempotency and graceful degradation.
6. Design for tenant isolation, auditability, privacy, data deletion and key rotation from the start.
7. Prefer boring, supported technologies and managed services when they reduce operational/security burden.
8. Do not introduce Kubernetes, microservices, graph databases, blockchain or LLMs without a measured requirement and operations plan.
9. Document system context, containers, deployment, data flows, trust boundaries and failure modes.
10. Architecture is a hypothesis until validated through threat modeling, load tests, cost modeling and operational exercises.
