# Verdict and scan state machine

Do not conflate execution status with threat assessment. Model them separately.

## Scan status candidates
`QUEUED`, `RUNNING`, `COMPLETED`, `PARTIAL`, `FAILED`, `EXPIRED`, `CANCELLED`.

## Threat verdict candidates
`MALICIOUS`, `SUSPICIOUS`, `BENIGN`, `UNKNOWN` (exact public labels and mappings require product research and ADR).

## Required rules
- `FAILED`, `PARTIAL`, stale evidence, provider outage, unsupported scheme or timeout must not automatically map to `BENIGN`.
- `UNKNOWN` is a valid result and should explain what is missing and what user action is prudent.
- Distinguish evidence confidence from risk score and recommended action.
- A benign assessment means available evidence did not indicate threat under defined coverage; it is not a guarantee of safety.
- Define state transitions, re-scan semantics, cache freshness, revocation, expiry and API compatibility.
- Ensure UI copy and color never overstate the underlying state.
