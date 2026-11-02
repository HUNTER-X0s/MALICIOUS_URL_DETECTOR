# Layered URL threat detection taxonomy

Candidate signal groups to evaluate independently:
1. Exact URL/domain/IP reputation and provider verdicts.
2. URL structure: scheme, length, entropy, path/query patterns, suspicious delimiters, encoded content and parser anomalies.
3. Host/domain: lexical similarity, brand typosquatting, punycode/IDN, Unicode confusables, subdomain abuse, domain age/registration evidence where lawfully available.
4. DNS/infrastructure: A/AAAA/CNAME/MX/NS/TXT, passive DNS where licensed, ASN, hosting and shared infrastructure.
5. TLS/certificate: certificate properties, issuance/CT context, hostname coverage and anomalies.
6. Redirect chain: hop count, destination transitions, cloaking, shorteners, open redirects and cross-domain pivots.
7. Webpage signals: DOM/HTML forms, credential collection, brand/logo similarity, scripts and content only inside isolated scanner.
8. File/download indicators: type, reputation and sandbox analysis only within specialized isolated workflows.
9. Campaign/graph context: relationships across domains, certificates, infrastructure, content and campaigns, subject to poisoning controls.
10. ML models: lexical, character/token, graph, visual and behavioural models, only when evaluation demonstrates value.
11. User/analyst feedback: corroborated labels with trust, abuse and appeal controls.

For each layer document coverage, latency, false-positive/negative profile, data freshness, provenance, licensing, evasion and outage behavior. Avoid additive score double counting of correlated signals.
