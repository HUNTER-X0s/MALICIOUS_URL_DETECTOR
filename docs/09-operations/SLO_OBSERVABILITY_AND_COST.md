# SLO, observability and unit economics

Define service-level indicators before selecting SLOs: API availability/latency, scan queue delay, verdict completion latency, provider freshness/availability, scanner isolation events, extension overhead, error rates, data integrity, and support response. Set SLO targets from user research, infrastructure and cost evidence; do not invent 99.99% promises.

Use structured logs, metrics, traces and audit events with correlation IDs. Redact URL credentials, sensitive query parameters, fragments, API keys and personal data. Apply sampling and retention controls. Alert on user impact, not noise. Maintain provider circuit breakers and health metrics.

Model per-scan cost by provider/API usage, DNS/TLS, compute, browser rendering, storage, bandwidth, support and abuse. Add tenant-level quotas, global budgets, cost alerts and safe degradation. Never let a public URL endpoint create unbounded third-party API spend.
