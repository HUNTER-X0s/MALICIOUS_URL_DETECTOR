# Abuse prevention and service safety

URLSentinel itself may be abused as an anonymous scanner, SSRF relay, denial-of-service amplifier, reconnaissance proxy, reputation laundering endpoint or source of sensitive URL leakage. Threat model the product as both defender and potential tool of abuse.

## Controls to evaluate
- Authentication or progressive friction for expensive/deep scan operations; low-risk basic checks may be anonymous only with strict quotas and abuse protection.
- Per-IP/account/tenant/global rate and concurrency limits, scan budget, queue fairness and provider spend caps.
- Prevent internal/private/metadata scanning at all layers; never expose a generic fetch or proxy API.
- Abuse detection for high-volume targets, repeated scans, credential guessing, scan loops, suspicious automation and API key sharing.
- Destination policies, deny/allow controls for special-use networks, and clear handling of internal corporate scanning only in a separately authorized enterprise design.
- Protect scan result endpoints from enumeration, cross-tenant access and public indexing.
- Prevent user reports from poisoning data: corroboration, reputation, review, audit, appeal and rollback.
- Keep provider API keys server-side; prevent usage/response forwarding that violates licensing.
- Expose safe abuse contact, acceptable-use policy, enforcement workflow and transparency on account restrictions.
- Set cost alarms and emergency kill switches for provider calls, scanning and high-cost model features.

## Enforcement quality
Do not silently punish legitimate users based on one heuristic. Define reason codes, escalation, false-positive appeal and support path. Log minimal abuse evidence with strict access and retention. Rate limits and blocks must not reveal sensitive internal detection rules unnecessarily.
