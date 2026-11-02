---
trigger: model_decision
description: "Apply these security requirements whenever designing, coding, reviewing, testing or operating any URLSentinel component or trust boundary."
---

# Security-first engineering

- Threat-model every trust boundary and externally reachable feature. Apply least privilege, zero trust and defence in depth.
- Never expose secrets, tokens, signed URLs or sensitive query values in logs, analytics, screenshots or prompts.
- No active untrusted URL fetching from the main API. Network analysis must use isolated workers and controlled egress.
- Block special-use IPv4/IPv6, loopback, private, link-local, multicast, reserved and metadata destinations; mitigate DNS rebinding/redirect pivots; validate actual connected peer.
- Never execute downloaded payloads on the host. Quarantine and isolate artifacts.
- Findings require severity, evidence, owner, remediation and regression test.
