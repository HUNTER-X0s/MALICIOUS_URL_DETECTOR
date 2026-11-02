---
name: url-processing
description: Implement safe, standards-aware URL parsing, canonicalization and feature extraction.
---

# URL processing

Preserve raw input securely and derive typed representations without losing evidence. Use standards-compliant parser behavior; document browser/server parser differences. Handle schemes, userinfo, ports, IPv4/IPv6 literals, IDNs, percent encoding, backslashes, dot segments, Unicode normalization, trailing dots, default ports and malformed inputs. Never over-normalize distinct URLs into collisions. Do not visit URLs in parsing code. Use property-based, differential and adversarial tests; preserve leading evidence and redact sensitive components in logs.
