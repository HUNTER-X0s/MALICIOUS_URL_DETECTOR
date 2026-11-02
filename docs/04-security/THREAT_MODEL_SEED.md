# Threat model seed

## Assets
User trust and decisions; submitted URLs; credentials/tokens embedded in URLs; account data; API keys; provider credentials; signing keys; verdict integrity; feed data; scanner workers; source code and CI/CD; customer/tenant data; audit evidence.

## Adversaries
Phishers, malware operators, bot operators, opportunistic attackers, malicious website operators, compromised providers, insider threats, poisoned-data contributors, malicious dependencies and compromised build/release credentials.

## Required threat areas
- SSRF and access to loopback/private/link-local/metadata/internal networks.
- DNS rebinding, split-horizon DNS, CNAME chains and redirect-to-private pivots.
- URL parser differential, userinfo confusion, scheme smuggling, IPv4 variants, IPv6 zone IDs, IDN homographs, Unicode confusables, percent-encoding and backslash ambiguity.
- Redirect loops, open redirect chains, huge responses, decompression bombs, slow responses and protocol downgrade.
- HTML/JS/browser exploit, download and document risk inside scanner.
- Scanner-to-host escape, network egress, mounted secrets and shared-kernel risks.
- Extension permissions, content-script isolation, message spoofing, service worker lifecycle, update supply chain and page-origin attacks.
- API authn/authz, IDOR, rate abuse, tenant leakage, replay and resource exhaustion.
- Threat-feed poisoning, label manipulation, stale data, provider outage and adversarial ML.
- Admin/account compromise, signing key compromise, CI/CD and dependency supply chain.
- Prompt injection in fetched webpages, repositories, issue comments, logs and files.

Antigravity must create feature-specific STRIDE/attack-tree/data-flow models, rank findings, add tests and record accepted residual risk. This seed is not a complete threat model.
