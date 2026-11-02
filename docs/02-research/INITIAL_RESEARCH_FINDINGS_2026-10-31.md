# Initial Research Findings — checked 2026-10-31

This is a bounded preparation-time research snapshot, not an exhaustive global survey. Recheck every changing product feature, license, API restriction and policy before implementation or launch.

## Antigravity operating model
Google documentation describes workspace rules and agent skills, planning artifacts, browser automation and agent-team capabilities. Availability differs by surface, plan and release. Verify current installed behaviour rather than relying on a static list of commands. Rules should hold durable invariants; skills should describe repeatable task procedures; project docs should contain detailed reference knowledge. Store output in Git rather than treating chat artifacts as the system of record.

Sources: https://antigravity.google/docs/rules/ ; https://antigravity.google/docs/skills/ ; https://antigravity.google/docs/planning/ ; https://antigravity.google/docs/browser/ ; https://antigravity.google/docs/agent-teams/

## Critical Antigravity rule/skill format finding
The official Rules documentation states that every Markdown file directly under `.agents/rules/` requires YAML frontmatter with a valid `trigger` (`always_on`, `model_decision`, `glob` or `manual`). A missing or invalid trigger can cause the rule to be silently discarded. `model_decision` rules require a description. Agent Skills require a `SKILL.md` with YAML frontmatter and a description; the workspace format uses both `name` and `description`. The starter package's initial rule files did not include the required rule frontmatter; this defect has been corrected in this revised package and all 12 rules have been validated for metadata presence.

Sources: https://antigravity.google/docs/rules/ ; https://antigravity.google/docs/skills/

## Threat-intelligence provider licensing
Google Safe Browsing API documentation states it is for non-commercial use; Google points commercial use cases toward Web Risk. Do not build a commercial product around an API tier whose terms prohibit the intended use. URLhaus is principally a malware URL feed/service and its terms and commercial use conditions must be reviewed. PhishTank is phishing-oriented and has API requirements/limits. These providers are not interchangeable, and one feed cannot establish a comprehensive safety verdict. Obtain current legal/contractual approval before production.

Sources: https://developers.google.com/safe-browsing ; https://cloud.google.com/web-risk ; https://urlhaus.abuse.ch/api/ ; https://phishtank.org/api_info.php

## Browser extension security and distribution
Chrome Web Store policies emphasize narrow permissions, transparency and truthful listing/data practices. Manifest V3 extension security and remote-code restrictions must be respected; do not ship remote executable code or create a remote command interpreter. Edge shares Chromium foundations but requires separate compatibility testing; Firefox WebExtensions and review policies differ. Store listing quality and discoverability are not equivalent to general web SEO.

Sources: https://developer.chrome.com/docs/webstore/program-policies/ ; https://developer.chrome.com/docs/extensions/develop/migrate/ ; https://learn.microsoft.com/en-us/microsoft-edge/extensions-chromium/ ; https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions ; https://extensionworkshop.com/documentation/publish/add-on-policies/

## Accessibility and web performance
W3C WCAG 2.2 is a W3C Recommendation and should inform web and extension accessibility work. Core Web Vitals are field metrics, not a guarantee of user-perceived zero latency; commonly published “good” thresholds are LCP <=2.5s, INP <200ms and CLS <0.1 at the 75th percentile. Measure real-user and lab results separately and tune by device/network.

Sources: https://www.w3.org/TR/WCAG22/ ; https://web.dev/articles/vitals

## SEO and discoverability
Search engine optimization concerns public crawlable website content. Chrome, Firefox and Edge are browsers, not separate web search engines with independent indexing rankings. Browser extension discoverability is handled through the relevant extension stores, their metadata, policies, reviews, quality and user trust. Do not promise first position or game ranking systems. Scan result pages and user-submitted URLs should not be publicly indexed by default.

Sources: https://developers.google.com/search/docs/fundamentals/seo-starter-guide ; https://developers.google.com/search/docs/essentials/spam-policies ; https://developer.chrome.com/docs/webstore/program-policies/

## Secure development
OWASP ASVS 5.0 provides application security verification requirements. OWASP Top 10:2025 is an awareness document, not a complete test plan. NIST SSDF SP 800-218 describes secure software development practices integrated throughout the SDLC. Use them as reference baselines; map applicable controls and demonstrate evidence rather than claiming certification.

Sources: https://owasp.org/www-project-application-security-verification-standard/ ; https://owasp.org/Top10/2025/ ; https://csrc.nist.gov/pubs/sp/800/218/final

## Research limitations
This package does not claim to have inspected every website, every product or every paper in existence. Such a survey is neither bounded nor meaningful. It establishes a reproducible research process and initial authoritative source map. Antigravity must perform targeted, ongoing research for each concrete product and architecture decision, include contrary evidence, and stop when the research decision has sufficient evidence.
