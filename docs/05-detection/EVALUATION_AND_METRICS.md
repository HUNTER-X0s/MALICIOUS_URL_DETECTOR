# Detection evaluation and metrics

## Outcomes
Track precision, recall, FPR, FNR, PR-AUC, ROC-AUC only where informative, calibration, coverage, abstention/UNKNOWN rate, detection delay, source freshness and per-segment quality. Report confidence intervals and sample sizes.

## Evaluation design
- Use licensed datasets with provenance, permitted purpose and documented labels.
- Time-split to emulate future threats; domain/campaign-disjoint splits to prevent leakage.
- Deduplicate and measure near duplicates. Avoid random splits that leak templates/campaigns.
- Include clean benign URLs and difficult benign lookalikes; measure false-positive cost.
- Report by language/script, TLD, geography, device, source and threat category where representative.
- Evaluate drift, feed outages, evasion and adversarial perturbation.
- Compare against baseline rules and provider outputs; avoid cherry-picking.
- Red-team model and threshold changes prior to rollout.

## Risk policy
Risk score and confidence are distinct. Thresholds must be calibrated for use case and action severity. High-impact blocks need stronger evidence than warnings. Unknown/incomplete scans must remain unknown. Define appeal and correction workflow.
