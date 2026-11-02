# Malicious URL and web-threat coverage matrix

This matrix is a research/evaluation taxonomy. It is not a claim that every class is currently detected. Antigravity should assess prevalence, user harm, data availability, legal feasibility, detection signals, evasion and test-set availability for each category.

## URL and host deception
- Typosquatting, homoglyphs, IDN/punycode and Unicode confusables.
- Brand impersonation, lookalike login pages, fake support/payment/account pages.
- Subdomain confusion, deceptive path/query/username segments, misleading ports and parser differentials.
- Alternate IP literals/encodings, IPv6 forms, unusual schemes and malformed URLs.
- URL shorteners, open redirects, chained redirects and multi-hop destination changes.
- Newly registered, disposable, parked, compromised or abandoned domains.

## Threat outcomes
- Credential harvesting and session/token theft.
- Malware distribution, exploit kits, drive-by download and unwanted software.
- Tech-support scams, fake update prompts, payment/invoice fraud and investment/romance/advance-fee scams.
- Fake CAPTCHA/social-engineering flows, browser notification abuse and deceptive permission requests.
- Phishing targeting consumer, enterprise, cloud, identity, collaboration and financial services.
- Malicious documents/downloads and file-hosting links (requires separate file-analysis scope).

## Infrastructure and delivery patterns
- Compromised legitimate websites, shared hosting/CDN abuse and cloud storage links.
- Fast-flux, DGAs, domain shadowing, DNS manipulation and changing infrastructure.
- Certificate/TLS context anomalies and certificate/infrastructure reuse.
- Geo-, time-, referrer-, cookie- or user-agent-dependent cloaking.
- Mobile-only, QR-delivered, messaging-delivered and email-delivered links.
- Campaign infrastructure and graph relationships across URLs, domains, certificates, IPs and content.

## Evasion and operational challenges
- Benign-looking URLs whose threat appears only after interaction or time delay.
- Redirect and content changes between scan time and click time (TOCTOU).
- Region- and browser-specific content, CAPTCHA and anti-bot responses.
- Low-volume, targeted and one-time URLs with little reputation history.
- Legitimate services abused as URL wrappers, redirects or hosted content.
- Adversarial text, homograph variations, encoding changes and feature manipulation.

## Cross-cutting test dimensions
Language/script, geography, TLD, mobile/desktop, browser, network conditions, threat age, campaign, source provider, scan depth, URL length/complexity, redirect count and evidence freshness. Ensure representative benign lookalikes to measure false positives.

## Coverage record per category
Track: priority; observed prevalence/source; user impact; detection method; available data/license; baseline performance; precision/recall/FPR/FNR; time-to-detect; freshness; segment gaps; evasion limitations; safety/abuse concerns; rollout status; owner; next research date. A category may be out of scope or unknown, but it must not be silently counted as covered.
