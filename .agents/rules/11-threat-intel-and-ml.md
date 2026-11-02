---
trigger: model_decision
description: "Apply these requirements when integrating threat-intelligence sources, building detection logic, training/evaluating ML or issuing risk verdicts."
---

# Threat intelligence and ML

- Track provider terms, license, quota, freshness, provenance, confidence and outage behaviour.
- Feed absence is not proof of safety.
- Prevent poisoning, duplicates, label/time leakage and train/test contamination. Use temporal/domain splits, calibration and drift monitoring.
- ML/LLM output is one signal, not unquestionable truth. Preserve explainability and abstention.
