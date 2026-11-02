# Safe URL handling baseline

## Parsing
- Treat submitted strings as hostile. Parse without fetching. Define accepted schemes; reject or explicitly classify unsupported schemes.
- Preserve raw input securely; create normalized representations with explicit transformations and parser version.
- Handle userinfo, ports, IP literals, alternate IPv4 forms, IPv6, trailing dots, IDNs, Unicode, percent-encoding, backslashes, dot segments, fragments and malformed authority.
- Use standards-aware libraries and differential tests against browser behavior; do not invent parser rules.

## Sensitive content
- Query values and fragments may include credentials, reset tokens, private identifiers or search terms. Redact by default in logs, analytics, URLs shared externally and support artifacts.
- Avoid storing full submitted URLs unless necessary, disclosed and protected with retention controls.

## Network access
- Parsing/lexical analysis should not access the network.
- Active checks must run behind a dedicated controlled boundary with default-deny egress, destination validation, connection-time IP checks and redirect revalidation.
- Deny non-public/special-use addresses and cloud metadata, including IPv4-mapped IPv6 and unusual encodings.
- Limit protocols/ports, redirects, DNS answers, body sizes, response time, concurrency and total scan budget.
- Re-resolve/revalidate each redirect and connection; do not trust a hostname string after validation.
- Do not follow URLs that resolve into internal infrastructure even if a prior hop was public.
- Do not forward cookies, user authorization, browser credentials or ambient headers.
- Do not execute downloaded files. Quarantine only where there is a documented isolated pipeline.

## Evidence
Capture minimal sanitized metadata, timestamp, destination class and failure reason. Avoid retaining response bodies by default. Make provider and scanner failures visible as incomplete/unknown, never benign.
