# Verdict contract seed

Keep the following concepts separate:
- `verdict`: one of a deliberately defined set such as `MALICIOUS`, `SUSPICIOUS`, `UNKNOWN`, `BENIGN` (exact naming requires ADR and compatibility review).
- `risk_score`: calibrated numeric estimate with documented meaning, not a universal truth.
- `confidence`: confidence in the assessment, separately calibrated or categorized.
- `evidence[]`: signal, source, timestamp, freshness, provenance, observation, reliability and contribution.
- `recommended_action`: safe user guidance distinct from verdict.
- `limitations[]`: unavailable sources, partial scan, unsupported scheme, stale cache and uncertainty.
- `checked_at`, `expires_at` and `contract_version`.

Do not equate no threat-feed hit with benign. Do not return SAFE/BENIGN solely because scanner/provider failed. Provide an explicit unknown/indeterminate/unavailable state. Avoid exposing sensitive internal heuristics if doing so enables evasion. Define compatibility, signing and redaction rules before finalizing schema.
