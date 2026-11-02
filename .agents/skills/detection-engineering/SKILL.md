---
name: detection-engineering
description: Design, implement and evaluate layered malicious URL detection.
---

# Detection engineering

Use complementary signals: exact/near reputation, lexical structure, host/domain, DNS/RDAP/WHOIS where lawful, TLS/certificates, redirect graph, page signals only in isolated scanning, brand/typosquatting, infrastructure relations and carefully evaluated ML. Track provenance, timestamp, freshness, confidence and provider coverage per signal. A feed miss is not benign evidence. Calibrate risk; distinguish verdict, confidence, evidence, freshness and action. Maintain abstention/UNKNOWN. Evaluate temporal and domain-disjoint generalization, class imbalance, false-positive costs, false negatives, drift and adversarial robustness. Save experiment cards and reproducible datasets.
