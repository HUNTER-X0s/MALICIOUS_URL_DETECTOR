---
name: secure-code-review
description: Perform a skeptical security and correctness review of changes.
---

# Secure code review

Review diff, requirements, threat model, authorization boundaries and data flow. Look for injection, SSRF, authn/authz flaws, IDOR, race conditions, path traversal, deserialization, unsafe parsing, secret leakage, weak crypto, insecure defaults, unsafe logging, resource exhaustion, tenant leakage, dependency issues and fail-open behavior. Trace inputs to sinks and verify negative cases. Check tests but do not treat test count as proof. Report severity, exploit preconditions, impact, evidence, fix and regression test. Independent review must not merely repeat author claims.
