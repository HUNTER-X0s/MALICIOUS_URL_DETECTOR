# ADR-005: Threat Intelligence Feed Ingestion and In-Memory Hash Lookup

**Status:** ACCEPTED  
**Date:** 2026-11-03  
**Deciders:** URLSentinel Autonomous Engineering  
**Consulted:** Detection Engineering, Security Engineering, Architecture

---

## Context
A real-time malicious URL protection platform must identify known active attacks with sub-millisecond latency without leaking user navigation to third parties on every request. URLhaus (abuse.ch) and OpenPhish provide high-fidelity feeds of malware distribution and credential phishing destinations.

## Decision
1. Implement local canonical hash indexing (`_URL_HASH_DATABASE` and `_DOMAIN_DATABASE`) using SHA-256 hashes of WHATWG-normalized URLs and hostnames.
2. Provide pre-seeded curated signatures of verified deceptive lures for offline reliability.
3. Ingest OpenPhish plain-text feed and URLhaus feeds with structured provenance tracking:
   - Source attribution (`source`)
   - Threat type (`threat_type`: phishing, malware_download, scam)
   - Reported timestamp (`reported_at`)
   - Explicit confidence rating (`confidence`: CRITICAL, HIGH)
4. Integrate threat hits directly into `evaluate_verdict` in `verdict_engine.py`, mapping verified feed matches immediately to `MALICIOUS` with full evidence disclosure.

## Alternatives Considered
- **Direct live external API calls on every scan**: Rejected because it introduces 200–800ms latency, leaks user queries to third parties, and fails when external APIs rate-limit or suffer outages.
- **Purely client-side lookup**: Rejected for the complete feed due to memory footprint in browser extensions; local caching of hits is used instead.

## Consequences
- **Positive:** Microsecond-latency exact matches; complete privacy preservation; verifiable provenance in verdict records.
- **Negative:** Requires background periodic feed polling (every 10–60 minutes) to maintain freshness.

