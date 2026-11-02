# Security test authorization and safe research policy

URLSentinel is a defensive product. Security testing must be scoped to owned code, local test fixtures, dedicated lab systems or third-party assets with written authorization.

Allowed by default: static review of this repository; dependency/configuration scanning; unit/integration security tests; fuzzing local parsers with synthetic input; tests against local mock HTTP/DNS/TLS servers; testing deployed staging assets owned by the project under an approved test plan.

Requires approval: penetration testing against external infrastructure; automated scanning of public websites; testing provider endpoints beyond documented API usage; load/stress tests against shared services; crawling competitors; collecting or uploading user/private URLs; publishing proof-of-concept exploit details; production testing.

Never: attack third-party systems without authorization, bypass access controls, steal credentials, deploy malware, execute malicious payloads on the host, evade provider limits, or use the scanner as a proxy into private/internal networks.

Every test plan specifies target owner, exact scope, time window, source IP, rate limits, allowed techniques, data handling, stop condition, contact, and cleanup.
