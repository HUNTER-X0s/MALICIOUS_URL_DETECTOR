---
name: browser-extension
description: Build secure and privacy-preserving browser extensions for Chromium and Firefox.
---

# Browser extension engineering

Research current store policies and browser API differences before choosing manifest/API strategy. Minimize permissions and host access; prefer optional permission flows. Keep executable logic packaged; no remote code, eval or arbitrary command delivery. Validate message sender, origin, schema, size and rate; defend against compromised pages and content-script injection. Avoid leaking browsing history or URL query secrets. Handle offline, stale verdicts and backend outages transparently. Test Chrome, Edge and Firefox separately, including install, update, content scripts, MV3 service worker suspension and accessibility. Maintain store listing/privacy declarations aligned with actual behavior.
