# Browser extension requirements seed

- Define supported browsers/versions and explicit compatibility matrix; Chromium commonality does not remove browser API differences.
- Request minimum permissions; use optional permissions and clear explanations when possible.
- Provide concise popup status, page-level warning where justified, settings, privacy controls and accessible keyboard interaction.
- Avoid collecting all browsing history by default. Minimize URL transmission and redact query/fragment where possible while preserving required detection semantics.
- Explain whether scanning is local, remote, delayed, stale or unavailable.
- Never block a URL based solely on a timeout or backend outage; define policy and user override safely.
- Defend content scripts, messages, service worker and storage; no remote executable code.
- Test lifecycle, suspended service worker, navigation race, SPA, private/incognito consent, browser updates, offline behavior, malicious page interference and store policy.
- Store listing must truthfully describe permissions, collection, sharing and functionality.
